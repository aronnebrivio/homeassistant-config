import datetime
import ssl

import requests
from waste_collection_schedule import Collection
from waste_collection_schedule.service.CMCityMedia import SERVICE_MAP

TITLE = "CM City Media - Müllkalender"
DESCRIPTION = "Source script for cmcitymedia.de"
URL = "https://cmcitymedia.de"
TEST_CASES = {
    "Blankenheim - Bezirk F: Lindweiler, Rohr": {"hpid": 415, "district": 1371},
    "Blankenheim": {"hpid": 415, "realmid": 41500},
    "Oberstadion": {"hpid": 447, "district": 1349},
}


def EXTRA_INFO():
    return [{"title": s["region"], "url": URL} for s in SERVICE_MAP]


API_URL = "https://sslslim.cmcitymedia.de/v1/{}/waste/{}/dates"
DATE_FORMAT = "%Y-%m-%d"


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


class Source:
    def __init__(self, hpid, realmid=None, district=None):
        self.hpid = hpid
        self.service = next(
            (item for item in SERVICE_MAP if item["hpid"] == self.hpid), None
        )
        self.realmid = realmid if realmid else self.service["realm"]
        self.district = district
        self.session = requests.Session()
        self.session.mount("https://", TLSAdapter())

    def fetch(self):

        entries = []

        district_param = f"?district={self.district}" if self.district else ""
        result = self.session.get(
            API_URL.format(self.hpid, self.service["realm"]) + district_param
        )

        result.raise_for_status()

        for item in result.json()["result"][1]["items"]:
            entries.append(
                Collection(
                    date=datetime.datetime.strptime(item["date"], DATE_FORMAT).date(),
                    t=item["name"],
                    icon=self.service["icons"][item["wastetype"]],
                )
            )

        return entries
