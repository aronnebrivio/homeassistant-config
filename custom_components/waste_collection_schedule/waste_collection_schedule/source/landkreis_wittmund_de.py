import json

import requests
from bs4 import BeautifulSoup
from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.exceptions import (
    SourceArgAmbiguousWithSuggestions,
    SourceArgumentNotFoundWithSuggestions,
)
from waste_collection_schedule.service.ICS import ICS

TITLE = "Landkreis Wittmund"
DESCRIPTION = "Source for Landkreis Wittmund waste collection."
URL = "https://www.landkreis-wittmund.de"
TEST_CASES = {
    "CityWithoutStreet": {
        "city": "Werdum",
    },
    "CityWithStreet": {
        "city": "Werdum",
        "street": "alle Straßen",
    },
}

API_URL = "https://www.landkreis-wittmund.de/Leben-Wohnen/Wohnen/Abfall/Abfuhrkalender/"
AUTOCOMPLETE_URL = "https://www.landkreis-wittmund.de/output/autocomplete.php?out=json&type=abto&mode=&select=2&refid={}&term="
DOWNLOAD_URL = "https://www.landkreis-wittmund.de/output/options.php?ModID=48&call=ical&ArtID%5B0%5D=3105.1&ArtID%5B1%5D=1.4&ArtID%5B2%5D=1.2&ArtID%5B3%5D=1.3&ArtID%5B4%5D=1.1&pois={}&alarm=0"


PARAM_TRANSLATIONS = {
    "de": {
        "city": "Ort",
        "street": "Straße",
    }
}


class Source:
    def __init__(self, city, street=None):
        self._city = city
        self._street = street
        self._ics = ICS()

    def fetch(self):
        cityId = self.fetch_city_id(self._city)
        streetId = self.fetch_street_id(cityId, self._street)

        return self.fetch_ics(DOWNLOAD_URL.format(streetId))

    def is_city_selection(self, tag, cityName):
        return tag["value"] != "" and tag.string == self._city

    def fetch_city_id(self, cityName):
        r = requests.get(API_URL)
        if not r.ok:
            raise Exception(f"Error: failed to fetch url: {API_URL}")

        soup = BeautifulSoup(r.text, "html.parser")
        citySelection = [
            a
            for a in soup.select("#sf_locid > option[value]")
            if self.is_city_selection(a, cityName)
        ]
        if len(citySelection) == 0:
            raise SourceArgumentNotFoundWithSuggestions(
                "city",
                cityName,
                {
                    a.string
                    for a in soup.select("#sf_locid > option[value]")
                    if a.get("value", "") != ""
                }
                - {None, ""},
            )

        if len(citySelection) > 1:
            raise SourceArgAmbiguousWithSuggestions(
                "city",
                cityName,
                {
                    a.string
                    for a in soup.select("#sf_locid > option[value]")
                    if a.get("value", "") != ""
                }
                - {None, ""},
            )

        return citySelection[0]["value"]

    def fetch_street_id(self, cityId, streetName):
        r = requests.get(
            AUTOCOMPLETE_URL.format(cityId, streetName), headers={"Referer": API_URL}
        )

        if not r.ok:
            raise Exception(
                "Error: failed to fetch url: {}".format(
                    AUTOCOMPLETE_URL.format(cityId, streetName)
                )
            )

        streets = json.loads(r.text)
        if streetName != None:
            streetId = [item[0] for item in streets if streetName in item[1]]
        else:
            streetId = [item[0] for item in streets]

        if len(streetId) == 0:
            raise SourceArgumentNotFoundWithSuggestions(
                "street", streetName, {item[1] for item in streets}
            )

        if len(streetId) > 1:
            raise SourceArgAmbiguousWithSuggestions(
                "street", streetName, {item[1] for item in streets}
            )

        return streetId[0]

    def fetch_ics(self, url):
        r = requests.get(url, headers={"Referer": API_URL})

        if not r.ok:
            raise Exception(f"Error: failed to fetch url: {url}")

        # parse ics file
        r.encoding = "utf-8"
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
