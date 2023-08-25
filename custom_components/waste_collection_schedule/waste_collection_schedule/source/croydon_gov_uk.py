# Credit where it's due:
# This is predominantly a refactoring of the Croydon Council script from the UKBinCollectionData repo
# https://github.com/robbrad/UKBinCollectionData

import json
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Croydon Council"
DESCRIPTION = "Source for croydon.gov.uk services for Croydon Council, UK."
URL = "https://croydon.gov.uk"

# Website stops responding if repeated queries are made in quick succession.
# Shouldn't be an issue in normal use where 1 query/day is made, but repeated HA restarts might cause the query to fail.
# When testing, it may be worth testing them individually by commenting out two of the test cases.
TEST_CASES = {
    "Test_001": {"postcode": "CR0 6LN", "houseID": "64 Coniston Road"},
    "Test_002": {"postcode": "SE25 5BU", "houseID": "23B Howard Road"},
    "Test_003": {"postcode": "CR0 6EG", "houseID": "48 Exeter Road"},
}
ICON_MAP = {
    "Food waste": "mdi:food",
    "General rubbish": "mdi:trash-can",
    "Paper and card recycling": "mdi:newspaper",
    "Glass, plastics, cans and cartons recycling": "mdi:bottle-wine",
}
API_URLS = {
    "BASE": "https://service.croydon.gov.uk",
    "CSRF": "/wasteservices/w/webpage/bin-day-enter-address",
    "SEARCH": "/wasteservices/w/webpage/bin-day-enter-address?webpage_subpage_id=PAG0000898EECEC1&webpage_token=faab02e1f62a58f7bad4c2ae5b8622e19846b97dde2a76f546c4bb1230cee044&widget_action=fragment_action",
    "SCHEDULE": "/wasteservices/w/webpage/bin-day-enter-address?webpage_subpage_id=PAG0000898EECEC1&webpage_token=faab02e1f62a58f7bad4c2ae5b8622e19846b97dde2a76f546c4bb1230cee044",
}
HEADER_COMPONENTS = {
    "BASE": {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "service.croydon.gov.uk",
        "Origin": API_URLS["BASE"],
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    },
    "GET": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Mode": "none",
    },
    "POST": {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Mode": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
    }
}
SESSION_STORAGE = {
    "destination_stack": [
        "w/webpage/bin-day-enter-address",
        "w/webpage/your-bin-collection-details?context_record_id=86086077"
        "&webpage_token=5c047b2c10b4aad66bef2054aac6bea52ad7a5e185ffdf7090b01f8ddc96728f",
        "w/webpage/bin-day-enter-address",
        "w/webpage/your-bin-collection-details?context_record_id=86085229"
        "&webpage_token=cf1b8fd6213f4823277d98c1dd8a992e6ebef1fabc7d892714e5d9dade448c37",
        "w/webpage/bin-day-enter-address",
        "w/webpage/your-bin-collection-details?context_record_id=86084221"
        "&webpage_token=7f52fb51019bf0e6bfe9647b1b31000124bd92a9d95781f1557f58b3ed40da52",
        "w/webpage/bin-day-enter-address",
        "w/webpage/your-bin-collection-details?context_record_id=86083209"
        "&webpage_token=de50c265da927336f526d9d9a44947595c3aa38965aa8c495ac2fb73d272ece8",
        "w/webpage/bin-day-enter-address",
    ],
    "last_context_record_id": "86086077",
}


class Source:
    def __init__(self, postcode, houseID):
        self._postcode = str(postcode).upper()
        self._houseID = str(houseID)


    def fetch(self):

        s = requests.Session()

        ### Get token
        csrf_token = ""
        url = API_URLS["BASE"] + API_URLS["CSRF"]
        headers = {**HEADER_COMPONENTS["BASE"],**HEADER_COMPONENTS["GET"]}
        r0 = s.get(url, headers=headers)
 
        soup = BeautifulSoup(r0.text, features="html.parser")
        app_body = soup.find("div", {"class": "app-body"})
        script = app_body.find("script", {"type": "text/javascript"}).string
        p = re.compile("var CSRF = ('|\")(.*?)('|\");")
        m = p.search(script)
        csrf_token = m.groups()[1]
        # print(csrf_token)

        ### Use postcode and houseID to find address
        addressID = "0"
        url = API_URLS["BASE"] + API_URLS["SEARCH"]
        headers = {**HEADER_COMPONENTS["BASE"], **HEADER_COMPONENTS["POST"],}
        form_data = {
            "code_action": "search",
            "code_params": '{"search_item":"' + self._postcode + '","is_ss":true}',
            "fragment_action": "handle_event",
            "fragment_id": "PCF0020408EECEC1",
            "fragment_collection_class": "formtable",
            "fragment_collection_editable_values": '{"PCF0021449EECEC1":"1"}',
            "_session_storage": json.dumps(
                {
                    "/wasteservices/w/webpage/bin-day-enter-address": {},
                    "_global": SESSION_STORAGE,
                }
            ),
            "action_cell_id": "PCL0005629EECEC1",
            "action_page_id": "PAG0000898EECEC1",
            "form_check_ajax": csrf_token,
        }
        r1 = s.post(url, headers=headers, data=form_data)

        addresses = json.loads(r1.text)["response"]["items"]
        for address in addresses:
            # print(address)
            if self._houseID in str(address["address_single_line"]):
                addressID = str(address["id"])
        # print(addressID)

        ### Use addressID to get schedule
        collection_data = ""
        url = API_URLS["BASE"] + API_URLS["SCHEDULE"]
        headers = {**HEADER_COMPONENTS["BASE"], **HEADER_COMPONENTS["POST"]}
        form_data = {
            "form_check": csrf_token,
            "submitted_page_id": "PAG0000898EECEC1",
            "submitted_widget_group_id": "PWG0002644EECEC1",
            "submitted_widget_group_type": "modify",
            "submission_token": "63e9126bacd815.12997577",
            "payload[PAG0000898EECEC1][PWG0002644EECEC1][PCL0005629EECEC1][formtable]"
            "[C_63e9126bacfb3][PCF0020408EECEC1]": addressID,
            "payload[PAG0000898EECEC1][PWG0002644EECEC1][PCL0005629EECEC1][formtable]"
            "[C_63e9126bacfb3][PCF0021449EECEC1]": "1",
            "payload[PAG0000898EECEC1][PWG0002644EECEC1][PCL0005629EECEC1][formtable]"
            "[C_63e9126bacfb3][PCF0020072EECEC1]": "Next",
            "submit_fragment_id": "PCF0020072EECEC1",
            "_session_storage": json.dumps({"_global": SESSION_STORAGE}),
            "_update_page_content_request": 1,
            "form_check_ajax": csrf_token,
        }
        r2 = s.post(url, headers=headers, data=form_data)
        
        json_response = json.loads(r2.text)
        url = API_URLS["BASE"] + json_response["redirect_url"]
        headers = {**HEADER_COMPONENTS["BASE"], **HEADER_COMPONENTS["POST"]}
        form_data = {
            "_dummy": 1,
            "_session_storage": json.dumps(
                {"_global": SESSION_STORAGE}
            ),
            "_update_page_content_request": 1,
            "form_check_ajax": csrf_token,
        }
        r3 = s.post(url, headers=headers, data=form_data)

        json_response = json.loads(r3.text)
        collection_data = json_response["data"]
        soup = BeautifulSoup(collection_data, features="html.parser")
        schedule = soup.find_all("div", {"class": "listing_template_record"})

        entries = []
        for pickup in schedule:
            waste_type = pickup.find_all("div", {"class": "fragment_presenter_template_show"})[0].text.strip()
            waste_date = pickup.find("div", {"class": "bin-collection-next"}).attrs["data-current_value"].strip()
            entries.append(
                Collection(
                    date=datetime.strptime(waste_date, "%d/%m/%Y %H:%M").date(),
                    t=waste_type,
                    icon=ICON_MAP.get(waste_type),
                )
            )


        return entries
