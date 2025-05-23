from __future__ import annotations

import collections
import json
import logging
import random
import time
from asyncio import run_coroutine_threadsafe
from collections import OrderedDict
from datetime import datetime

import aiohttp
import homeassistant.core as ha_core
import pychromecast
import spotipy
from homeassistant.components.cast.helpers import ChromeCastZeroconf
from homeassistant.exceptions import HomeAssistantError
from requests import TooManyRedirects
from .spotify_controller import SpotifyController
from .error import TokenError
from .const import CONF_SP_DC, CONF_SP_KEY
from .helpers import get_cast_devices, get_spotify_devices, get_spotify_media_player, query_from_url
from .spotify_controller import SpotifyController
from .crypto import get_totp

_LOGGER = logging.getLogger(__name__)


class SpotifyCastDevice:
    """Represents a spotify device."""

    hass = None
    castDevice = None
    spotifyController = None

    def __init__(
        self, hass: ha_core.HomeAssistant, call_device_name: str, call_entity_id: str
    ) -> None:
        """Initialize a spotify cast device."""
        self.hass = hass

        # Get device name from either device_name or entity_id
        device_name = None
        if call_device_name is None:
            entity_id = call_entity_id
            if entity_id is None:
                raise HomeAssistantError(
                    "Either entity_id or device_name must be specified"
                )
            entity_states = hass.states.get(entity_id)
            if entity_states is None:
                _LOGGER.error("Could not find entity_id: %s", entity_id)
            else:
                device_name = entity_states.attributes.get("friendly_name")
        else:
            device_name = call_device_name

        if device_name is None or device_name.strip() == "":
            raise HomeAssistantError("device_name is empty")

        # Find chromecast device
        self.castDevice = self.get_chromecast_device(device_name)
        _LOGGER.debug("Found cast device: %s", self.castDevice)
        self.castDevice.wait()

    def get_chromecast_device(self, device_name: str) -> None:
        # Get cast from discovered devices of cast platform
        known_devices = get_cast_devices(self.hass)

        _LOGGER.debug("Chromecast devices: %s", known_devices)
        cast_info = next(
            (
                castinfo
                for castinfo in known_devices
                if castinfo.friendly_name == device_name
            ),
            None,
        )
        _LOGGER.debug("cast info: %s", cast_info)
        if cast_info:
            return pychromecast.get_chromecast_from_cast_info(
                cast_info.cast_info, ChromeCastZeroconf.get_zeroconf()
            )
        _LOGGER.error(
            "Could not find device %s from hass.data",
            device_name,
        )
        raise HomeAssistantError(
            "Could not find device with name {}".format(device_name)
        )

    def start_spotify_controller(self, access_token: str, expires: int):
        sp = SpotifyController(self.castDevice, access_token, expires)
        self.castDevice.register_handler(sp)
        sp.launch_app()

        if not sp.is_launched and not sp.credential_error:
            raise HomeAssistantError(
                "Failed to launch spotify controller due to timeout"
            )
        if not sp.is_launched and sp.credential_error:
            raise HomeAssistantError(
                "Failed to launch spotify controller due to credentials error"
            )

        self.spotifyController = sp

    def get_spotify_device_id(self, user_id) -> None:
        spotify_media_player = get_spotify_media_player(self.hass, user_id)
        max_retries = 5
        counter = 0
        devices_available = None
        _LOGGER.debug(
            "Searching for Spotify device: {}".format(
                self.spotifyController.device)
        )
        while counter < max_retries:
            devices_available = get_spotify_devices(
                spotify_media_player,
                self.hass
            )
            # Look for device to make sure we can start playback
            for device in devices_available:
                if device.device_id == self.spotifyController.device:
                    _LOGGER.debug(
                        "Found matching Spotify device: {}".format(device)
                    )
                    return device.device_id

            sleep = random.uniform(1.5, 1.8) ** counter
            time.sleep(sleep)
            counter = counter + 1

        _LOGGER.error(
            'No device with id "{}" known by Spotify'.format(
                self.spotifyController.device
            )
        )
        _LOGGER.error("Known devices: {}".format(devices_available))

        raise HomeAssistantError("Failed to get device id from Spotify")


class SpotifyToken:
    """Represents a spotify token for an account."""

    hass = None
    sp_dc = None
    sp_key = None
    _access_token = None
    _token_expires = 0

    def __init__(self, hass: ha_core.HomeAssistant, sp_dc: str, sp_key: str):
        self.hass = hass
        self.sp_dc = sp_dc
        self.sp_key = sp_key
        self.totp = get_totp()

    def ensure_token_valid(self) -> bool:
        if float(self._token_expires) > time.time():
            return True
        self.get_spotify_token()

    @property
    def access_token(self) -> str:
        self.ensure_token_valid()
        _LOGGER.debug("expires: %s time: %s", self._token_expires, time.time())
        return self._access_token

    def get_spotify_token(self) -> tuple[str, int]:
        try:
            self._access_token, self._token_expires = run_coroutine_threadsafe(
                self.start_session(), self.hass.loop
            ).result()
            expires = self._token_expires - int(time.time())
            return self._access_token, expires
        except TooManyRedirects:
            _LOGGER.error(
                "Could not get spotify token. sp_dc and sp_key could be "
                "expired. Please update in config."
            )
            raise HomeAssistantError("Expired sp_dc, sp_key")
        except (TokenError, Exception) as exc:  # noqa: E722
            raise HomeAssistantError(exc)

    @property
    def headers(self) -> dict:
        """Provides the generic headers for api requests"""
        return {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 "
                "Safari/537.36"
            ),
            "Accept": "application/json",
        }

    async def start_session(self, max_retries=5):
        """ Starts session to get access token. """
        cookies = {"sp_dc": self.sp_dc, "sp_key": self.sp_key}

        async with aiohttp.ClientSession(cookies=cookies) as session:

            # get server time
            async with session.get(
                url="https://open.spotify.com/server-time",
                headers=self.headers,
            ) as response:
                data = await response.json()
                server_time = data["serverTime"]

            totp_value = self.totp.at(server_time)

            retry_count = 0

            while True:

                async with session.get(
                    url="https://open.spotify.com/get_access_token",
                    allow_redirects=False,
                    headers=self.headers,
                    params={
                        "reason": "transport",
                        "productType": "web-player",
                        "totp": totp_value,
                        "totpServer": totp_value,
                        "totpVer": 5,
                        "sTime": server_time,
                        "cTime": server_time,
                    }
                ) as response:
                    data = await response.text()
                    headers = response.headers
                    status = response.status

                try:
                    self.raise_for_status(status, data, headers)
                    data = json.loads(data)
                    await self._test_token(session, data["accessToken"])
                    break
                except (HomeAssistantError, TokenError) as exc:
                    if retry_count >= max_retries - 1:
                        raise exc
                    retry_count += 1

        access_token = data["accessToken"]
        expires_timestamp = data["accessTokenExpirationTimestampMs"]
        expiration_date = int(expires_timestamp) // 1000

        return access_token, expiration_date

    def raise_for_status(self, status: int, content: str, headers: dict):
        """Raises an error for invalid response"""

        location_query = query_from_url(headers.get("Location"))

        if status == 302 and location_query.get("_authfailed", "0") == "1":
            _LOGGER.error(
                "Unsuccessful token request, received code 302 and "
                "Location header %s. sp_dc and sp_key could be "
                "expired. Please update in config.",
                headers["Location"],
            )
            raise HomeAssistantError("Expired sp_dc, sp_key")
        if status != 200:
            _LOGGER.info(
                "Unsuccessful token request, received code %i", status
            )
            raise TokenError()

    async def _test_token(self, session: aiohttp.ClientSession, token: str):
        """Test the token in the session provided"""

        headers = self.headers
        headers |= {"Authorization": f"Bearer {token}"}

        async with session.get(
            url="https://api.spotify.com/v1/me",
            headers=headers
        ) as response:
            await response.json()

        if not response.ok:
            _LOGGER.debug("Token received is not valid. Retrying")
            raise TokenError("Token received is not valid. Retrying")


class SpotcastController:

    spotifyTokenInstances = {}
    accounts: dict = {}
    hass = None

    def __init__(
        self,
        hass: ha_core.HomeAssistant,
        sp_dc: str,
        sp_key: str,
        accs: collections.OrderedDict,
    ) -> None:
        if accs:
            self.accounts = accs
        self.accounts["default"] = OrderedDict(
            [("sp_dc", sp_dc), ("sp_key", sp_key)])
        self.hass = hass

    def get_token_instance(self, account: str = None) -> any:
        """Get token instance for account"""
        if account is None:
            account = "default"

        # TODO: add error logging when user provide invalid account
        # name
        dc = self.accounts.get(account).get(CONF_SP_DC)
        key = self.accounts.get(account).get(CONF_SP_KEY)

        _LOGGER.debug("setting up with  account %s", account)
        if account not in self.spotifyTokenInstances:
            self.spotifyTokenInstances[account] = SpotifyToken(
                self.hass, dc, key)
        return self.spotifyTokenInstances[account]

    def get_spotify_client(self, account: str) -> spotipy.Spotify:
        return spotipy.Spotify(auth=self.get_token_instance(account).access_token)

    def _getSpotifyConnectDeviceId(self, client, device_name):
        media_player = get_spotify_media_player(
            self.hass, client._get("me")["id"])
        devices_available = get_spotify_devices(media_player, self.hass)
        for device in devices_available:
            if device.name == device_name:
                return device.device_id
        return None

    def get_spotify_device_id(self, account, spotify_device_id, device_name, entity_id):
        # login as real browser to get powerful token
        access_token, expires = self.get_token_instance(
            account).get_spotify_token()
        # get the spotify web api client
        client = spotipy.Spotify(auth=access_token)
        # first, rely on spotify id given in config
        if not spotify_device_id:
            # if not present, check if there's a spotify connect device
            # with that name
            spotify_device_id = self._getSpotifyConnectDeviceId(
                client, device_name)
        if not spotify_device_id:
            # if still no id available, check cast devices and launch
            # the app on chromecast
            spotify_cast_device = SpotifyCastDevice(
                self.hass,
                device_name,
                entity_id,
            )
            me_resp = client._get("me")
            spotify_cast_device.start_spotify_controller(access_token, expires)
            # Make sure it is started
            spotify_device_id = spotify_cast_device.get_spotify_device_id(
                me_resp["id"])
        return spotify_device_id

    def play(
        self,
        client: spotipy.Spotify,
        spotify_device_id: str,
        uri: str,
        random_song: bool,
        position: str,
        ignore_fully_played: str,
        position_ms: str,
        country_code: str = None
    ) -> None:
        _LOGGER.debug(
            "Playing URI: %s on device-id: %s",
            uri,
            spotify_device_id,
        )

        if uri.find("show") > 0:
            show_episodes_info = client.show_episodes(uri, market=country_code)
            if show_episodes_info and len(show_episodes_info["items"]) > 0:
                if ignore_fully_played:
                    for episode in show_episodes_info["items"]:
                        if not episode["resume_point"]["fully_played"]:
                            episode_uri = episode["external_urls"]["spotify"]
                            break
                else:
                    episode_uri = show_episodes_info["items"][0]["external_urls"][
                        "spotify"
                    ]
                _LOGGER.debug(
                    (
                        "Playing episode using uris (latest podcast playlist)="
                        " for uri: %s"
                    ),
                    episode_uri,
                )
                client.start_playback(
                    device_id=spotify_device_id, uris=[episode_uri], position_ms=position_ms)
        elif uri.find("episode") > 0:
            _LOGGER.debug("Playing episode using uris= for uri: %s", uri)
            client.start_playback(device_id=spotify_device_id, uris=[
                                  uri], position_ms=position_ms)

        elif uri.find("track") > 0:
            _LOGGER.debug("Playing track using uris= for uri: %s", uri)
            client.start_playback(device_id=spotify_device_id, uris=[
                                  uri], position_ms=position_ms)
        else:
            if uri == "random":
                _LOGGER.debug(
                    "Cool, you found the easter egg with playing a random" " playlist"
                )
                playlists = client.user_playlists("me", 50)
                no_playlists = len(playlists["items"])
                uri = playlists["items"][random.randint(
                    0, no_playlists - 1)]["uri"]
            kwargs = {"device_id": spotify_device_id,
                      "context_uri": uri, "position_ms": position_ms}

            if random_song:
                if uri.find("album") > 0:
                    results = client.album_tracks(uri, market=country_code)
                    position = random.randint(0, int(results["total"]) - 1)
                elif uri.find("playlist") > 0:
                    results = client.playlist_tracks(uri)
                    position = random.randint(0, int(results["total"]) - 1)
                elif uri.find("collection") > 0:
                    results = client.current_user_saved_tracks()
                    position = random.randint(0, int(results["total"]) - 1)
                _LOGGER.debug(
                    "Start playback at random position: %s", position)
            if uri.find("artist") < 1:
                kwargs["offset"] = {"position": position}
            _LOGGER.debug(
                (
                    'Playing context uri using context_uri for uri: "%s" '
                    "(random_song: %s)"
                ),
                uri,
                random_song,
            )
            client.start_playback(**kwargs)

    def get_playlists(
        self,
        account: str,
        playlist_type: str,
        country_code: str,
        locale: str,
        limit: int,
    ) -> dict:
        client = self.get_spotify_client(account)
        resp = {}

        if playlist_type == "discover-weekly":
            playlist_type = "made-for-x"

        if playlist_type == "user" or playlist_type == "default" or playlist_type == "":
            resp = client.current_user_playlists(limit=limit)

        elif playlist_type == "featured":
            resp = client.featured_playlists(
                locale=locale,
                country=country_code,
                timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                limit=limit,
                offset=0,
            )
            resp = resp.get("playlists")
        else:
            resp = client._get(
                "views/" + playlist_type,
                content_limit=limit,
                locale=locale,
                platform="web",
                types="album,playlist,artist,show,station",
                limit=limit,
                offset=0,
            )
            resp = resp.get("content")

        return resp
