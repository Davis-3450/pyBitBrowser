from dataclasses import dataclass
from enum import Enum

from bit_browser.models import client
from bit_browser.models.browser import Browser


class Status(Enum):
    open = "open"
    closed = "closed"


@dataclass
class Session:
    id: str
    status: Status
    browser: Browser


class BrowserManager:
    def __init__(self):
        self.browsers: list[Session] = []
        self.client = client

    def _helper(self):
        self._get_all_browsers()

    def _get_all_browsers(self) -> None:
        """_summary_"""
        o: list[Session] = []
        pass
