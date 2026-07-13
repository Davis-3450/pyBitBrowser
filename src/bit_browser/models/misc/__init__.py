from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from bit_browser.models.base import APIModel


class BrowserIdsRequest(APIModel):
    ids: List[str]


class BrowserIdRequest(APIModel):
    id: str


class CloseBySeqsRequest(APIModel):
    seqs: List[int]


class WindowBoundsFlexibleRequest(APIModel):
    seqlist: Optional[List[int]] = None


class WindowBoundsRequest(APIModel):
    type: Optional[str] = None
    startX: Optional[int] = None
    startY: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    col: Optional[int] = None
    spaceX: Optional[int] = None
    spaceY: Optional[int] = None
    offsetX: Optional[int] = None
    offsetY: Optional[int] = None
    seqlist: Optional[List[int]] = None
    screenId: Optional[int] = None


class ProxyUpdateRequest(APIModel):
    ids: List[str]
    ipCheckService: str
    proxyMethod: int
    proxyType: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    proxyUserName: Optional[str] = None
    proxyPassword: Optional[str] = None
    dynamicIpUrl: Optional[str] = None
    dynamicIpChannel: Optional[str] = None
    isDynamicIpChangeIp: Optional[bool] = None
    isGlobalProxyInfo: Optional[bool] = None
    isIpv6: Optional[bool] = None


class UpdateRemarkRequest(APIModel):
    browserIds: List[str]
    remark: str


class CheckAgentRequest(APIModel):
    host: str
    port: str
    proxyType: str
    proxyUserName: Optional[str] = None
    proxyPassword: Optional[str] = None
    checkExists: Optional[int] = None


class BrowserOpenRequest(APIModel):
    id: str
    args: Optional[List[str]] = None
    queue: Optional[bool] = None


class AutopasteRequest(APIModel):
    browserId: str
    url: str


class ReadFileRequest(APIModel):
    filepath: str


class CookiesSetRequest(APIModel):
    browserId: str
    cookies: List[dict[str, Any]]


class CookiesClearRequest(APIModel):
    browserId: str
    saveSynced: bool = True


class CookiesFormatRequest(APIModel):
    cookie: Any
    hostname: Optional[str] = None


class RpaRequest(APIModel):
    id: str
