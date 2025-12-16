from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from bit_browser.models.base import APIModel


class BrowserFingerprint(APIModel):
    # Response object (many more fields exist; extras are allowed)
    id: Optional[str] = None
    seq: Optional[int] = None
    browserId: Optional[str] = None
    coreVersion: Optional[str] = None
    ostype: Optional[str] = None
    os: Optional[str] = None
    osVersion: Optional[str] = None
    userAgent: Optional[str] = None


class BrowserProfile(APIModel):
    # Response profile (list/detail). Fields are intentionally mostly optional.
    id: Optional[str] = None
    seq: Optional[int] = None
    code: Optional[str] = None
    platform: Optional[str] = None
    platformIcon: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = None
    remark: Optional[str] = None
    userName: Optional[str] = None
    password: Optional[str] = None
    cookie: Optional[str] = None

    proxyMethod: Optional[int] = None
    proxyType: Optional[str] = None
    host: Optional[str] = None
    port: Optional[Any] = None
    proxyUserName: Optional[str] = None
    proxyPassword: Optional[str] = None

    groupId: Optional[str] = None
    status: Optional[int] = None
    ip: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None

    browserFingerPrint: Optional[BrowserFingerprint] = None


class BrowserListData(APIModel):
    totalNum: int = 0
    list: List[BrowserProfile] = Field(default_factory=list)


class BrowserOpenData(APIModel):
    ws: str
    http: str
    coreVersion: Optional[str] = None
    driver: Optional[str] = None
    seq: Optional[int] = None
    name: Optional[str] = None
    remark: Optional[str] = None
    groupId: Optional[str] = None
    pid: Optional[int] = None

class BrowserUpdateRequest(APIModel):
    # /browser/update (create or update when id is set)
    id: Optional[str] = None
    groupId: Optional[str] = None
    platform: Optional[str] = None
    platformIcon: Optional[str] = None
    url: Optional[str] = None
    name: str
    remark: Optional[str] = None
    userName: Optional[str] = None
    password: Optional[str] = None
    cookie: Optional[str] = None

    proxyMethod: int = 2
    proxyType: str = "noproxy"
    host: Optional[str] = None
    port: Optional[Any] = None
    proxyUserName: Optional[str] = None
    proxyPassword: Optional[str] = None

    ip: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None

    # docs: can be {} for random, so keep as dict
    browserFingerPrint: dict[str, Any] = Field(default_factory=dict)


class BrowserPartialUpdateRequest(APIModel):
    ids: List[str]
    browserFingerPrint: dict[str, Any] = Field(default_factory=dict)


# Backwards-compat aliases
Browser = BrowserProfile
CreateBrowser = BrowserUpdateRequest
