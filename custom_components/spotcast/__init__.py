"""main module for spotcast homeassistant utility"""

from __future__ import annotations

__version__ = "4.0.1"

import collections
import logging
import time

import homeassistant.core as ha_core
from homeassistant.components import websocket_api
from homeassistant.const import CONF_ENTITY_ID, CONF_OFFSET, CONF_REPEAT
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_ACCOUNTS,
    CONF_DEVICE_NAME,
    CONF_FORCE_PLAYBACK,
    CONF_IGNORE_FULLY_PLAYED,
    CONF_RANDOM,
    CONF_SHUFFLE,
    CONF_SP_DC,
    CONF_SP_KEY,
    CONF_SPOTIFY_ACCOUNT,
    CONF_SPOTIFY_ALBUM_NAME,
    CONF_SPOTIFY_ARTIST_NAME,
    CONF_SPOTIFY_AUDIOBOOK_NAME,
    CONF_SPOTIFY_CATEGORY,
    CONF_SPOTIFY_COUNTRY,
    CONF_SPOTIFY_DEVICE_ID,
    CONF_SPOTIFY_EPISODE_NAME,
    CONF_SPOTIFY_GENRE_NAME,
    CONF_SPOTIFY_LIMIT,
    CONF_SPOTIFY_PLAYLIST_NAME,
    CONF_SPOTIFY_SHOW_NAME,
    CONF_SPOTIFY_TRACK_NAME,
    CONF_SPOTIFY_URI,
    CONF_START_VOL,
    DOMAIN,
    SCHEMA_PLAYLISTS,
    SCHEMA_WS_ACCOUNTS,
    SCHEMA_WS_CASTDEVICES,
    SCHEMA_WS_DEVICES,
    SCHEMA_WS_PLAYER,
    CONF_START_POSITION,
    SERVICE_START_COMMAND_SCHEMA,
    SPOTCAST_CONFIG_SCHEMA,
    WS_TYPE_SPOTCAST_ACCOUNTS,
    WS_TYPE_SPOTCAST_CASTDEVICES,
    WS_TYPE_SPOTCAST_DEVICES,
    WS_TYPE_SPOTCAST_PLAYER,
    WS_TYPE_SPOTCAST_PLAYLISTS,
)
from .helpers import (
    add_tracks_to_queue,
    async_wrap,
    get_cast_devices,
    get_random_playlist_from_category,
    get_search_results,
    get_spotify_devices,
    get_spotify_install_status,
    get_spotify_media_player,
    is_empty_str,
    is_valid_uri,
    url_to_spotify_uri,
)
from .spotcast_controller import SpotcastController

CONFIG_SCHEMA = SPOTCAST_CONFIG_SCHEMA
DEBUG = True

_LOGGER = logging.getLogger(__name__)


def setup(hass: ha_core.HomeAssistant, config: collections.OrderedDict) -> bool:
    """setup method for integration with Home Assistant

    Args:
        hass (ha_core.HomeAssistant): the HomeAssistant object of the
            server
        config (collections.OrderedDict): the configuration of the
            server

    Returns:
        bool: returns a bollean based on if the setup wroked or not
    """

    # get spotify core integration status
    # if return false, could indicate a bad spotify integration. Race
    # condition doesn't permit us to abort setup, see #258
    if not get_spotify_install_status(hass):
        _LOGGER.debug(
            "Spotify integration was not found, please verify integration is "
            "functionnal. Could result in python error..."
        )

    # Setup the Spotcast service.
    conf = config[DOMAIN]

    sp_dc = conf[CONF_SP_DC]
    sp_key = conf[CONF_SP_KEY]
    accounts = conf.get(CONF_ACCOUNTS)

    spotcast_controller = SpotcastController(hass, sp_dc, sp_key, accounts)

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["controller"] = spotcast_controller

    @callback
    def websocket_handle_playlists(
            hass: ha_core.HomeAssistant,
            connection,
            msg: str
    ):
        @async_wrap
        def get_playlist():
            """Handle to get playlist"""
            playlist_type = msg.get("playlist_type")
            country_code = msg.get("country_code")
            locale = msg.get("locale", "en")
            limit = msg.get("limit", 10)
            account = msg.get("account", None)

            _LOGGER.debug("websocket_handle_playlists msg: %s", msg)
            resp = spotcast_controller.get_playlists(
                account, playlist_type, country_code, locale, limit
            )
            connection.send_message(
                websocket_api.result_message(msg["id"], resp))

        hass.async_add_job(get_playlist())

    @callback
    def websocket_handle_devices(
            hass: ha_core.HomeAssistant,
            connection,
            msg: str,
    ):
        @async_wrap
        def get_devices():
            """Handle to get devices. Only for default account"""
            account = msg.get("account", None)
            client = spotcast_controller.get_spotify_client(account)
            me_resp = client._get("me")  # pylint: disable=W0212
            spotify_media_player = get_spotify_media_player(
                hass, me_resp["id"])
            resp = get_spotify_devices(spotify_media_player, hass)
            connection.send_message(
                websocket_api.result_message(msg["id"], resp))

        hass.async_add_job(get_devices())

    @callback
    def websocket_handle_player(
            hass: ha_core.HomeAssistant,
            connection,
            msg: str,
    ):
        @async_wrap
        def get_player():
            """Handle to get player"""
            account = msg.get("account", None)
            _LOGGER.debug("websocket_handle_player msg: %s", msg)
            client = spotcast_controller.get_spotify_client(account)
            resp = client._get("me/player")  # pylint: disable=W0212
            connection.send_message(
                websocket_api.result_message(msg["id"], resp))

        hass.async_add_job(get_player())

    @callback
    def websocket_handle_accounts(
            hass: ha_core.HomeAssistant,
            connection,
            msg: str,
    ):
        """Handle to get accounts"""
        _LOGGER.debug("websocket_handle_accounts msg: %s", msg)
        resp = list(accounts.keys()) if accounts is not None else []
        resp.append("default")
        connection.send_message(websocket_api.result_message(msg["id"], resp))

    @callback
    def websocket_handle_castdevices(
            hass: ha_core.HomeAssistant,
            connection, msg: str
    ):
        """Handle to get cast devices for debug purposes"""
        _LOGGER.debug("websocket_handle_castdevices msg: %s", msg)

        known_devices = get_cast_devices(hass)
        _LOGGER.debug("%s", known_devices)
        resp = [
            {
                "uuid": str(cast_info.cast_info.uuid),
                "model_name": cast_info.cast_info.model_name,
                "friendly_name": cast_info.cast_info.friendly_name,
            }
            for cast_info in known_devices
        ]

        connection.send_message(websocket_api.result_message(msg["id"], resp))

    def start_casting(call: ha_core.ServiceCall):
        """service called."""
        uri = call.data.get(CONF_SPOTIFY_URI)
        category = call.data.get(CONF_SPOTIFY_CATEGORY)
        country = call.data.get(CONF_SPOTIFY_COUNTRY)
        limit = call.data.get(CONF_SPOTIFY_LIMIT)
        artistName = call.data.get(CONF_SPOTIFY_ARTIST_NAME)
        albumName = call.data.get(CONF_SPOTIFY_ALBUM_NAME)
        playlistName = call.data.get(CONF_SPOTIFY_PLAYLIST_NAME)
        trackName = call.data.get(CONF_SPOTIFY_TRACK_NAME)
        showName = call.data.get(CONF_SPOTIFY_SHOW_NAME)
        episodeName = call.data.get(CONF_SPOTIFY_EPISODE_NAME)
        audiobookName = call.data.get(CONF_SPOTIFY_AUDIOBOOK_NAME)
        genreName = call.data.get(CONF_SPOTIFY_GENRE_NAME)
        random_song = call.data.get(CONF_RANDOM, False)
        repeat = call.data.get(CONF_REPEAT, False)
        shuffle = call.data.get(CONF_SHUFFLE, False)
        start_volume = call.data.get(CONF_START_VOL)
        spotify_device_id = call.data.get(CONF_SPOTIFY_DEVICE_ID)
        position = call.data.get(CONF_OFFSET)
        start_position = call.data.get(CONF_START_POSITION)
        force_playback = call.data.get(CONF_FORCE_PLAYBACK)
        account = call.data.get(CONF_SPOTIFY_ACCOUNT)
        ignore_fully_played = call.data.get(CONF_IGNORE_FULLY_PLAYED)
        device_name = call.data.get(CONF_DEVICE_NAME)
        entity_id = call.data.get(CONF_ENTITY_ID)

        try:  # yes this is ugly, quick fix while working on V4

            # if no market information try to get global setting
            if is_empty_str(country):
                try:
                    country = config[DOMAIN][CONF_SPOTIFY_COUNTRY]
                except KeyError:
                    country = None

            client = spotcast_controller.get_spotify_client(account)

            # verify the uri provided and clean-up if required
            if not is_empty_str(uri):

                # remove ? from badly formatted URI
                uri = uri.split("?")[0]

                if uri.startswith("http"):
                    try:
                        u = url_to_spotify_uri(uri)
                        _LOGGER.debug(
                            "converted web URL %s to spotify URI %s", uri, u)
                        uri = u
                    except ValueError:
                        _LOGGER.error(
                            "invalid web URL provided, could not convert to spotify URI: %s", uri)

                if not is_valid_uri(uri):
                    _LOGGER.error("Invalid URI provided, aborting casting")
                    return

                # force first two elements of uri to lowercase
                uri = uri.split(":")
                uri[0] = uri[0].lower()
                uri[1] = uri[1].lower()
                uri = ":".join(uri)

            # first, rely on spotify id given in config otherwise get one
            if not spotify_device_id:
                spotify_device_id = spotcast_controller.get_spotify_device_id(
                    account, spotify_device_id, device_name, entity_id
                )

            if start_position is not None:
                start_position *= 1000

            if (
                is_empty_str(uri)
                and len(
                    list(
                        filter(
                            lambda x: not is_empty_str(x),
                            [
                                artistName,
                                playlistName,
                                trackName,
                                showName,
                                episodeName,
                                audiobookName,
                                genreName,
                                category,
                            ],
                        )
                    )
                )
                == 0
            ):
                _LOGGER.debug("Transfering playback")
                current_playback = client.current_playback()
                if current_playback is not None:
                    _LOGGER.debug("Current_playback from spotify: %s",
                                  current_playback)
                    force_playback = True
                _LOGGER.debug("Force playback: %s", force_playback)
                client.transfer_playback(
                    device_id=spotify_device_id, force_play=force_playback
                )
            elif not is_empty_str(category):
                uri = get_random_playlist_from_category(
                    client, category, country, limit)

                if uri is None:
                    _LOGGER.error("No playlist returned. Stop service call")
                    return None

                spotcast_controller.play(
                    client,
                    spotify_device_id,
                    uri,
                    random_song,
                    position,
                    ignore_fully_played,
                    start_position,
                )
            else:
                searchResults = []
                if is_empty_str(uri):
                    # get uri from search request
                    searchResults = get_search_results(
                        spotify_client=client,
                        limit=limit,
                        artistName=artistName,
                        country=country,
                        albumName=albumName,
                        playlistName=playlistName,
                        trackName=trackName,
                        showName=showName,
                        episodeName=episodeName,
                        audiobookName=audiobookName,
                        genreName=genreName,
                    )
                    # play the first track
                    if len(searchResults) > 0:
                        uri = searchResults[0]["uri"]

                spotcast_controller.play(
                    client,
                    spotify_device_id,
                    uri,
                    random_song,
                    position,
                    ignore_fully_played,
                    start_position,
                )

                if len(searchResults) > 1:
                    add_tracks_to_queue(client, searchResults[1:])

            if start_volume <= 100:
                _LOGGER.debug("Setting volume to %d", start_volume)
                time.sleep(2)
                client.volume(volume_percent=start_volume,
                              device_id=spotify_device_id)
            if shuffle:
                _LOGGER.debug("Turning shuffle on")
                time.sleep(3)
                client.shuffle(state=shuffle, device_id=spotify_device_id)
            if repeat:
                _LOGGER.debug("Turning repeat on")
                time.sleep(3)
                client.repeat(state=repeat, device_id=spotify_device_id)

        except Exception as exc:
            if DEBUG:
                raise exc

            raise HomeAssistantError(exc) from exc

    # Register websocket and service
    websocket_api.async_register_command(
        hass=hass,
        command_or_handler=WS_TYPE_SPOTCAST_PLAYLISTS,
        handler=websocket_handle_playlists,
        schema=SCHEMA_PLAYLISTS,
    )
    websocket_api.async_register_command(
        hass=hass,
        command_or_handler=WS_TYPE_SPOTCAST_DEVICES,
        handler=websocket_handle_devices,
        schema=SCHEMA_WS_DEVICES,
    )
    websocket_api.async_register_command(
        hass=hass,
        command_or_handler=WS_TYPE_SPOTCAST_PLAYER,
        handler=websocket_handle_player,
        schema=SCHEMA_WS_PLAYER,
    )

    websocket_api.async_register_command(
        hass=hass,
        command_or_handler=WS_TYPE_SPOTCAST_ACCOUNTS,
        handler=websocket_handle_accounts,
        schema=SCHEMA_WS_ACCOUNTS,
    )

    websocket_api.async_register_command(
        hass=hass,
        command_or_handler=WS_TYPE_SPOTCAST_CASTDEVICES,
        handler=websocket_handle_castdevices,
        schema=SCHEMA_WS_CASTDEVICES,
    )

    hass.services.register(
        domain=DOMAIN,
        service="start",
        service_func=start_casting,
        schema=SERVICE_START_COMMAND_SCHEMA,
    )

    return True
