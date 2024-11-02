from datetime import datetime

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "North Lanarkshire Council"
DESCRIPTION = "Source for waste collection services for North Lanarkshire Council"
URL = "https://northlanarkshire.gov.uk"

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": "The easiest way to get the source arguments is to look at the url of the web page that displays your collection schedule. The url has the format: `www.northlanarkshire.gov.uk/bin-collection-dates/UPRN/USRN`",
}

PARAM_TRANSLATIONS = {
    "en": {
        "uprn": "Unique Property Reference Number (UPRN)",
        "usrn": "Unique Street Reference Number (USRN)",
    }
}

PARAM_DESCRIPTIONS = {
    "en": {
        "usrn": "Your Unique Street Reference Number (USRN) can be found by searching for your address at https://uprn.uk/ and viewing the _Data Associations_ section.",
        "uprn": "Alternatively, an easy way to discover your Unique Property Reference Number (UPRN) is by going to https://www.findmyaddress.co.uk/ and entering in your address details",
    }
}

TEST_CASES = {
    "Test_001": {
        "uprn": "118026605",
        "usrn": "48406574",
    },
    "Test_002": {
        "uprn": 118177268,
        "usrn": 48410258,
    },
    "Test_003": {
        "uprn": "000118035256",
        "usrn": "48409125",
    },
}


ICON_MAP = {
    "General Waste": "mdi:trash-can",
    "Blue-lidded Recycling Bin": "mdi:recycle",
    "Food and Garden": "mdi:leaf",
    "Glass, Metals, Plastics and Cartons": "mdi:glass-fragile",
}


class Source:
    def __init__(self, uprn: str | int, usrn: str | int):
        self._uprn = str(uprn).zfill(12)
        self._usrn = str(usrn)

    def fetch(self):
        s = requests.Session()

        r = s.get(
            f"https://www.northlanarkshire.gov.uk/bin-collection-dates/{self._uprn}/{self._usrn}"
        )
        r.raise_for_status

        soup = BeautifulSoup(r.text, "html.parser")
        containers = soup.findAll("div", {"class": "waste-type-container"})

        entries = []
        for idx, container in enumerate(containers):
            waste_type = container.find("h3").text
            waste_days = container.findAll("p")
            for day in waste_days:
                entries.append(
                    Collection(
                        date=datetime.strptime(day.text, "%d %B %Y").date(),
                        t=waste_type,
                        icon=ICON_MAP.get(waste_type),
                    )
                )

        return entries
