import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Moyne Shire Council"
DESCRIPTION = "Source for Moyne Shire Council rubbish collection."
URL = "https://www.moyne.vic.gov.au"
TEST_CASES = {"Test": {"street_address": "1 Cox Street, PORT FAIRY, 3284"}}

_LOGGER = logging.getLogger(__name__)

ICON_MAP = {
    "Landfill": "mdi:trash-can",
    "Recycling": "mdi:recycle",
    "FOGO": "mdi:leaf",
    "Glass Only": "mdi:BottleWine",
}


class Source:
    def __init__(self, street_address):
        self._street_address = street_address

    def fetch(self):
        session = requests.Session()

        response = session.get(
            "https://www.moyne.vic.gov.au/Your-property/Waste-and-recycling/Kerbside-collection-dates"
        )
        response.raise_for_status()

        response = session.get(
            "https://www.moyne.vic.gov.au/api/v1/myarea/search",
            params={"keywords": self._street_address},
        )
        response.raise_for_status()
        addressSearchApiResults = response.json()
        if (
            addressSearchApiResults["Items"] is None
            or len(addressSearchApiResults["Items"]) < 1
        ):
            raise Exception(
                f"Address search for '{self._street_address}' returned no results. Check your address on https://www.moyne.vic.gov.au/Your-property/Waste-and-recycling/Kerbside-collection-dates"
            )

        addressSearchTopHit = addressSearchApiResults["Items"][0]
        _LOGGER.debug("Address search top hit: %s", addressSearchTopHit)

        geolocationid = addressSearchTopHit["Id"]
        _LOGGER.debug("Geolocationid: %s", geolocationid)

        response = session.get(
            "https://www.moyne.vic.gov.au/ocapi/Public/myarea/wasteservices?ocsvclang=en-AU",
            params={"geolocationid": geolocationid},
        )
        response.raise_for_status()

        wasteApiResult = response.json()
        _LOGGER.debug("Waste API result: %s", wasteApiResult)

        soup = BeautifulSoup(wasteApiResult["responseContent"], "html.parser")

        entries = []
        for article in soup.find_all("article"):
            waste_type = article.h3.string
            icon = ICON_MAP.get(waste_type)
            next_pickup = article.find(class_="next-service").string
            if next_pickup is None:
                continue
            date_match = re.search(r"\d{1,2}\/\d{1,2}\/\d{4}", next_pickup)
            if date_match:
                next_pickup_date = datetime.strptime(
                    date_match.group(0), "%d/%m/%Y"
                ).date()
                entries.append(
                    Collection(date=next_pickup_date, t=waste_type, icon=icon)
                )

        return entries
