from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set

from prettyprinter import pprint

from bit_browser.client import client
from bit_browser.models.browser import Browser


class Status(Enum):
    open = "open"
    closed = "closed"


@dataclass
class Session:
    browser_id: str
    status: Status
    browser: Browser


class BrowserManager:
    def __init__(self):
        self.client = client
        self.sessions: dict[str, Session] = {}

    def _helper(self):
        self._get_all_browsers()

    def _get_all_browsers(self) -> None:
        """Get all browsers from the API and populate self.browsers."""

        page = 0
        seen = 0

        while True:
            r = self.client.list_browsers(page=page)

            total_num = r.get("totalNum", 0)  # total
            current_page_list: list = r["list"]

            for browser in current_page_list:
                b_id = browser["id"]

                if b_id in self.sessions.keys():
                    continue

                b = Browser(**browser)
                s = Session(browser_id=b_id, browser=b, status=Status.closed)
                self.sessions[b_id] = s

                seen += 1

            if seen >= total_num:
                break

            page += 1

    def _get_browser(self, browser_id: str) -> Session | None:
        r = self.client.get_browser_details(browser_id)
        if r:
            pass  # TODO - implement
        return None
