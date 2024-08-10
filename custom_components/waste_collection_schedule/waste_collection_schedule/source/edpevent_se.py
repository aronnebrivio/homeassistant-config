import json
import logging
from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "EDPEvent - Multi Source"
DESCRIPTION = "Source for all EDPEvent waste collection sources. This included multiple municipalities in Sweden."
URL = "https://www.edpevent.se"
TEST_CASES = {
    "Boden - Bodens Kommun": {
        "street_address": "KYRKGATAN 24",
        "service_provider": "boden",
    },
    "Boden - Gymnasiet": {
        "street_address": "IDROTTSGATAN 4",
        "url": "https://edpmobile.boden.se/FutureWeb/SimpleWastePickup",
    },
    "Uppsalavatten - Test1": {
        "street_address": "SADELVÄGEN 1",
        "url": "https://futureweb.uppsalavatten.se/Uppsala/FutureWeb/SimpleWastePickup",
    },
    "Uppsalavatten - Test2": {
        "street_address": "BJÖRKLINGE-GRÄNBY 33",
        "service_provider": "uppsalavatten",
    },
    "Uppsalavatten - Test3": {
        "street_address": "BJÖRKLINGE-GRÄNBY 20",
        "service_provider": "uppsalavatten",
    },
    "SSAM - Home": {
        "street_address": "Asteroidvägen 1, Växjö",
        "service_provider": "ssam",
    },
    "SSAM - Slambrunn": {
        "street_address": "Svanebro Ormesberga, Ör",
        "service_provider": "ssam",
    },
    "Skelleftea - Test1": {
        "street_address": "Frögatan 76 -150",
        "service_provider": "skelleftea",
    },
}

COUNTRY = "se"
_LOGGER = logging.getLogger(__name__)

# This maps the icon based on the waste type
ICON_MAP = {
    "Brännbart": "mdi:trash-can",
    "Matavfall tätt": "mdi:food",
    "Deponi": "mdi:recycle",
    "Restavfall": "mdi:trash-can",
    "Matavfall": "mdi:food-apple",
    "Slam": "",
    "Trädgårdsavfall": "mdi:leaf",
}

# This can be used to rename the waste types to something more user friendly
WASTE_TYPE_REPLACEMENTS = {
    "FNI1": "Kärl 1",
    "FNI2": "Kärl 2",
}

MONTH_MAP = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "Maj": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Okt": 10,
    "Nov": 11,
    "Dec": 12,
}

SERVICE_PROVIDERS = {
    "skelleftea": {
        "title": "Skellefteå",
        "url": "https://skelleftea.se",
        "api_url": "https://wwwtk2.skelleftea.se/FutureWeb/SimpleWastePickup",
    },
    "boden": {
        "title": "Boden",
        "url": "https://boden.se",
        "api_url": "https://edpmobile.boden.se/FutureWeb/SimpleWastePickup",
    },
    "ssam": {
        "title": "SSAM Södra Smalånds Avfall & Miljö",
        "url": "https://ssam.se",
        "api_url": "https://edpfuture.ssam.se/FutureWeb/SimpleWastePickup",
    },
    "uppsalavatten": {
        "title": "Uppsala Vatten",
        "url": "https://uppsalavatten.se",
        "api_url": "https://futureweb.uppsalavatten.se/Uppsala/FutureWeb/SimpleWastePickup",
    },
}

EXTRA_INFO = [
    {
        "title": data["title"],
        "url": data["url"],
        "default_params": {"service_provider": provider},
    }
    for provider, data in SERVICE_PROVIDERS.items()
]


class Source:
    def __init__(
        self,
        street_address: str,
        service_provider: str | None = None,
        url: str | None = None,
    ):
        self._street_address = street_address
        self._url = url
        # Check if the user provided a url
        if url is None:
            # Raise an exception if the user did not provide a service provider (or url)
            if service_provider is None:
                raise ValueError("You must provide either a service provider or a url")
            # Get the api url using the service provider
            self._url = SERVICE_PROVIDERS.get(service_provider.lower(), {}).get(
                "api_url"
            )
        if self._url is None:
            raise ValueError(
                f"Unknown service provider: {service_provider}, use one of {[x for x in SERVICE_PROVIDERS.keys()]}"
            )
        # Remove trailing slash from the url if present
        if self._url.endswith("/"):
            self._url = self._url[:-1]

    def fetch(self):
        params = {"searchText": self._street_address}
        # Use the street address to find the full street address with the building ID
        searchUrl = self._url + "/SearchAdress"
        # Search for the address
        response = requests.post(searchUrl, params=params, timeout=30)

        address_data = json.loads(response.text)
        address = None
        # Make sure the response is valid and contains data
        if address_data and len(address_data) > 0:
            # Check if the request was successful
            if address_data["Succeeded"]:
                # The request can be successful but still not return any buildings at the specified address
                if len(address_data["Buildings"]) > 0:
                    address = address_data["Buildings"][0]
                else:
                    raise Exception(
                        f"No returned building address for: {self._street_address}"
                    )
            else:
                raise Exception(
                    f"The server failed to fetch the building data for: {self._street_address}"
                )

        # Raise exception if all the above checks failed
        if not address:
            raise Exception(
                f"Failed to find building address for: {self._street_address}"
            )

        # Use the address we got to get the waste collection schedule
        params = {"address": address}
        getUrl = self._url + "/GetWastePickupSchedule"
        # Get the waste collection schedule
        response = requests.get(getUrl, params=params, timeout=30)

        data = json.loads(response.text)

        entries = []
        for item in data["RhServices"]:
            waste_type = ""
            next_pickup = item["NextWastePickup"]
            try:
                if "v" in next_pickup:
                    date_parts = next_pickup.split()
                    month = MONTH_MAP[date_parts[1]]
                    date_joined = "-".join([date_parts[0], str(month), date_parts[2]])
                    next_pickup_date = datetime.strptime(
                        date_joined, "v%W-%m-%Y"
                    ).date()
                elif not next_pickup:
                    continue
                else:
                    next_pickup_date = datetime.strptime(next_pickup, "%Y-%m-%d").date()
            except ValueError:
                # In some cases the date is just a month, so parse this as the
                # first of the month to at least get something close
                try:
                    next_pickup_date = datetime.strptime(next_pickup, "%b %Y").date()
                except ValueError as month_parse_error:
                    _LOGGER.warning(
                        "Failed to parse date %s, %s,",
                        next_pickup,
                        str(month_parse_error),
                    )
                    continue

            waste_type_prefix = item["WasteType"]
            if item["WasteType"] in WASTE_TYPE_REPLACEMENTS:
                waste_type_prefix = WASTE_TYPE_REPLACEMENTS[item["WasteType"]]
            waste_type = (
                waste_type_prefix
                + ", "
                + item["BinType"]["ContainerType"]
                + " "
                + str(item["BinType"]["Size"])
                + item["BinType"]["Unit"]
            )
            # Get the icon for the waste type, default to help icon if not found
            icon = ICON_MAP.get(item["WasteType"], "mdi:help")

            found = found = any(
                x.date == next_pickup_date and x.type == waste_type for x in entries
            )
            if not found:
                entries.append(
                    Collection(date=next_pickup_date, t=waste_type, icon=icon)
                )
        return entries
