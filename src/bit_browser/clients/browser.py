from __future__ import annotations

from typing import Any, Optional, Sequence, TypeVar

import requests

from bit_browser.constants import HEADERS, URL
from bit_browser.errors import (
    APIError,
    HTTPStatusError,
    NetworkError,
    ResponseDecodeError,
    ResponseValidationError,
)
from bit_browser._compat import model_dump, model_validate
from bit_browser.models.base import APIResponse
from bit_browser.models.browser import (
    BrowserListData,
    BrowserOpenData,
    BrowserPartialUpdateRequest,
    BrowserProfile,
    BrowserUpdateRequest,
)
from bit_browser.models.extralog import ExtralogItem, ExtralogListData
from bit_browser.models.group import Group, GroupListData
from bit_browser.models.misc import (
    AutopasteRequest,
    BrowserIdRequest,
    BrowserIdsRequest,
    BrowserOpenRequest,
    CheckAgentRequest,
    CloseBySeqsRequest,
    CookiesClearRequest,
    CookiesFormatRequest,
    CookiesSetRequest,
    ProxyUpdateRequest,
    ReadFileRequest,
    RpaRequest,
    UpdateRemarkRequest,
    WindowBoundsFlexibleRequest,
)

# Docs
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档


class BrowserClient:
    def __init__(self, url=URL, headers=HEADERS, token: Optional[str] = None):
        """
        Initialize the BrowserClient with optional API token.

        Args:
            url (str, optional): URL Defaults to URL.
            headers (dict, optional): Headers Defaults to HEADERS.
            token (Optional[str], optional): Token Defaults to None.
        """
        self.token = token
        self.url = url
        self.headers = headers.copy()
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.headers.update({"x-api-key": token}) if token else None

    def _post(
        self,
        endpoint: str,
        payload: dict | None = None,
        *,
        timeout: float | None = 10.0,
    ) -> Any:
        url = f"{self.url}{endpoint}"
        try:
            response = self.session.post(url, json=(payload or {}), timeout=timeout)
        except requests.RequestException as e:  # pragma: no cover
            raise NetworkError(str(e)) from e

        if not response.ok:
            raise HTTPStatusError(response.status_code, response.text)

        try:
            body = response.json()
        except ValueError as e:
            raise ResponseDecodeError(response.text) from e

        api = model_validate(APIResponse[Any], body)
        if not api.success:
            raise APIError(api.msg, data=api.data)
        return api.data

    def _post_typed(
        self,
        endpoint: str,
        payload: dict | None,
        model: type[T],
        *,
        timeout: float | None = 10.0,
    ) -> T:
        data = self._post(endpoint, payload, timeout=timeout)
        try:
            return model_validate(model, data)
        except Exception as e:
            raise ResponseValidationError(str(e)) from e

    @staticmethod
    def _payload(obj: Any) -> dict[str, Any]:
        if obj is None:
            return {}
        if isinstance(obj, dict):
            return obj
        return model_dump(obj, by_alias=True, exclude_none=True)

    # --- Browser Profiles ---
    def browser_update(self, request: BrowserUpdateRequest | dict[str, Any]) -> Any:
        return self._post("/browser/update", self._payload(request))

    def browser_update_typed(
        self, request: BrowserUpdateRequest | dict[str, Any]
    ) -> BrowserProfile:
        return self._post_typed(
            "/browser/update", self._payload(request), BrowserProfile
        )

    def browser_update_partial(
        self, request: BrowserPartialUpdateRequest | dict[str, Any]
    ) -> Any:
        return self._post("/browser/update/partial", self._payload(request))

    def browser_update_partial_typed(
        self, request: BrowserPartialUpdateRequest | dict[str, Any]
    ) -> Any:
        # API returns varying structures; keep Any but validate request typing.
        return self._post("/browser/update/partial", self._payload(request))

    def browser_open(self, request: BrowserOpenRequest | dict[str, Any]) -> Any:
        return self._post("/browser/open", self._payload(request))

    def browser_open_typed(
        self, request: BrowserOpenRequest | dict[str, Any]
    ) -> BrowserOpenData:
        return self._post_typed(
            "/browser/open", self._payload(request), BrowserOpenData
        )

    def browser_close(self, request: BrowserIdRequest | dict[str, Any]) -> Any:
        return self._post("/browser/close", self._payload(request))

    def browser_delete(self, request: BrowserIdRequest | dict[str, Any]) -> Any:
        return self._post("/browser/delete", self._payload(request))

    def browser_detail(self, request: BrowserIdRequest | dict[str, Any]) -> Any:
        return self._post("/browser/detail", self._payload(request))

    def browser_detail_typed(self, request: BrowserIdRequest | dict[str, Any]) -> BrowserProfile:
        return self._post_typed("/browser/detail", self._payload(request), BrowserProfile)

    def users_reset_closed_state(self, request: BrowserIdRequest | dict[str, Any]) -> Any:
        return self._post("/users", self._payload(request))

    # Backwards-compat alias; prefer `browser_update*`
    def _edit_browser(
        self,
        name: str,
        remark: str,
        proxy_method: int,
        browser_id: str | None = None,
        proxy_type: str = "noproxy",
        host: str = "",
        port: str = "",
        proxy_user_name: str = "",
        core_version: str = "112",
        browser_fingerprint: dict | None = None,
        extra: dict | None = None,
        **kwargs: Any,
    ):
        req = BrowserUpdateRequest(
            name=name,
            remark=remark,
            proxyMethod=proxy_method,
            proxyType=proxy_type,
            host=host or None,
            port=port or None,
            proxyUserName=proxy_user_name or None,
            id=browser_id or kwargs.get("id"),
            browserFingerPrint=browser_fingerprint or {"coreVersion": core_version},
        )
        payload = self._payload(req)
        if extra:
            payload.update(extra)
        return self._post("/browser/update", payload)

    # Backwards-compat wrappers (kept for existing callers)
    def create_or_update_browser(self, **kwargs: Any) -> Any:
        return self.browser_update(kwargs)

    def create_browser(self, payload: BrowserUpdateRequest | dict[str, Any]) -> Any:
        return self.browser_update(payload)

    def update_browsers(self, ids: list[str], remark: str) -> Any:
        req = BrowserPartialUpdateRequest(ids=ids, browserFingerPrint={})
        payload = self._payload(req)
        payload["remark"] = remark
        return self._post("/browser/update/partial", payload)

    def update_browser_partial(self, ids: Sequence[str], **fields) -> Any:
        payload: dict[str, Any] = {"ids": list(ids)}
        payload.update(fields)
        return self._post("/browser/update/partial", payload)

    def open_browser(self, browser_id: str, args: list[str] | None = None, queue: bool | None = None) -> Any:
        payload: dict[str, Any] = {"id": browser_id}
        if args is not None:
            payload["args"] = args
        if queue is not None:
            payload["queue"] = queue
        return self.browser_open(payload)

    def close_browser(self, browser_id: str) -> Any:
        return self.browser_close({"id": browser_id})

    def delete_browser(self, browser_id: str) -> Any:
        return self.browser_delete({"id": browser_id})

    def get_browser_details(self, browser_id: str) -> Any:
        return self.browser_detail({"id": browser_id})

    def reset_closed_state(self, browser_id: str) -> Any:
        return self.users_reset_closed_state({"id": browser_id})

    # Additional documented endpoints
    def list_browsers(self, page: int = 0, page_size: int = 100, **filters) -> Any:
        data = {"page": page, "pageSize": page_size}
        data.update(filters)
        return self._post("/browser/list", data)

    def list_browsers_typed(self, page: int = 0, page_size: int = 100, **filters) -> BrowserListData:
        data = {"page": page, "pageSize": page_size}
        data.update(filters)
        return self._post_typed("/browser/list", data, BrowserListData)

    def windowbounds_reset(self, **window_bounds) -> Any:
        # type, startX, startY, width, height, col, spaceX, spaceY, offsetX, offsetY
        return self._post("/windowbounds", window_bounds)

    def windowbounds_flexible(self, seqlist: Sequence[int] | None = None) -> Any:
        req = WindowBoundsFlexibleRequest(seqlist=list(seqlist) if seqlist is not None else None)
        return self._post("/windowbounds/flexable", self._payload(req))

    def get_all_displays(self) -> Any:
        return self._post("/alldisplays")

    def rpa_run(self, task_id: str) -> Any:
        return self._post("/rpa/run", self._payload(RpaRequest(id=task_id)))

    def rpa_stop(self, task_id: str) -> Any:
        return self._post("/rpa/stop", self._payload(RpaRequest(id=task_id)))

    def autopaste(self, browser_id: str, url: str) -> Any:
        return self._post("/autopaste", self._payload(AutopasteRequest(browserId=browser_id, url=url)))

    def utils_read_excel(self, filepath: str) -> Any:
        return self._post("/utils/readexcel", self._payload(ReadFileRequest(filepath=filepath)))

    def utils_read_file(self, filepath: str) -> Any:
        return self._post("/utils/readfile", self._payload(ReadFileRequest(filepath=filepath)))

    def cookies_set(self, browser_id: str, cookies: list[dict]) -> Any:
        return self._post("/browser/cookies/set", self._payload(CookiesSetRequest(browserId=browser_id, cookies=cookies)))

    def cookies_get(self, browser_id: str) -> Any:
        return self._post("/browser/cookies/get", {"browserId": browser_id})

    def cookies_clear(self, browser_id: str, save_synced: bool = True) -> Any:
        return self._post("/browser/cookies/clear", self._payload(CookiesClearRequest(browserId=browser_id, saveSynced=save_synced)))

    def cookies_format(self, cookie: str | list[dict], hostname: str | None = None) -> Any:
        return self._post("/browser/cookies/format", self._payload(CookiesFormatRequest(cookie=cookie, hostname=hostname)))

    def fingerprint_random(self, browser_id: str) -> Any:
        return self._post("/browser/fingerprint/random", {"browserId": browser_id})

    def clear_cache(self, ids: list[str]) -> Any:
        return self._post("/cache/clear", {"ids": ids})

    def clear_cache_except_extensions(self, ids: list[str]) -> Any:
        return self._post("/cache/clear/exceptExtensions", {"ids": ids})

    def get_opened_ports(self) -> Any:
        return self._post("/browser/ports")

    def get_all_pids(self) -> Any:
        return self._post("/browser/pids/all")

    def get_pids(self, ids: Sequence[str]) -> Any:
        return self._post("/browser/pids", {"ids": list(ids)})

    def delete_browsers_by_ids(self, ids: list[str]) -> Any:
        return self._post("/browser/delete/ids", self._payload(BrowserIdsRequest(ids=ids)))

    def close_by_seqs(self, seqs: Sequence[int]) -> Any:
        return self._post("/browser/close/byseqs", self._payload(CloseBySeqsRequest(seqs=list(seqs))))

    def close_all(self) -> Any:
        return self._post("/browser/close/all")

    def update_group(self, group_id: str, browser_ids: Sequence[str]) -> Any:
        return self._post(
            "/browser/group/update",
            {"groupId": group_id, "browserIds": list(browser_ids)},
        )

    # Groups (/group/*)
    def group_list(self, page: int = 0, page_size: int = 10) -> Any:
        return self._post("/group/list", {"page": page, "pageSize": page_size})

    def group_list_typed(self, page: int = 0, page_size: int = 10) -> GroupListData:
        return self._post_typed("/group/list", {"page": page, "pageSize": page_size}, GroupListData)

    def group_add(self, group_name: str, sort_num: int | None = None) -> Any:
        data: dict[str, Any] = {"groupName": group_name}
        if sort_num is not None:
            data["sortNum"] = sort_num
        return self._post("/group/add", data)

    def group_add_typed(self, group_name: str, sort_num: int | None = None) -> Group:
        data: dict[str, Any] = {"groupName": group_name}
        if sort_num is not None:
            data["sortNum"] = sort_num
        return self._post_typed("/group/add", data, Group)

    def group_edit(
        self, group_id: str, group_name: str, sort_num: int | None = None
    ) -> Any:
        data: dict[str, Any] = {"id": group_id, "groupName": group_name}
        if sort_num is not None:
            data["sortNum"] = sort_num
        return self._post("/group/edit", data)

    def group_edit_typed(self, group_id: str, group_name: str, sort_num: int | None = None) -> Group:
        data: dict[str, Any] = {"id": group_id, "groupName": group_name}
        if sort_num is not None:
            data["sortNum"] = sort_num
        return self._post_typed("/group/edit", data, Group)

    def group_delete(self, group_id: str) -> Any:
        return self._post("/group/delete", {"id": group_id})

    def group_delete_typed(self, group_id: str) -> Any:
        return self._post("/group/delete", {"id": group_id})

    def group_detail(self, group_id: str) -> Any:
        return self._post("/group/detail", {"id": group_id})

    def group_detail_typed(self, group_id: str) -> Group:
        return self._post_typed("/group/detail", {"id": group_id}, Group)

    def update_proxy(
        self,
        ids: Sequence[str],
        ip_check_service: str,
        proxy_method: int,
        proxy_type: str | None = None,
        host: str | None = None,
        port: int | None = None,
        proxy_user_name: str | None = None,
        proxy_password: str | None = None,
        dynamic_ip_url: str | None = None,
        dynamic_ip_channel: str | None = None,
        is_dynamic_ip_change_ip: bool | None = None,
        is_global_proxy_info: bool | None = None,
        is_ipv6: bool | None = None,
    ) -> Any:
        data: dict[str, Any] = {
            "ids": list(ids),
            "ipCheckService": ip_check_service,
            "proxyMethod": proxy_method,
        }
        if proxy_type is not None:
            data["proxyType"] = proxy_type
        if host is not None:
            data["host"] = host
        if port is not None:
            data["port"] = port
        if proxy_user_name is not None:
            data["proxyUserName"] = proxy_user_name
        if proxy_password is not None:
            data["proxyPassword"] = proxy_password
        if dynamic_ip_url is not None:
            data["dynamicIpUrl"] = dynamic_ip_url
        if dynamic_ip_channel is not None:
            data["dynamicIpChannel"] = dynamic_ip_channel
        if is_dynamic_ip_change_ip is not None:
            data["isDynamicIpChangeIp"] = is_dynamic_ip_change_ip
        if is_global_proxy_info is not None:
            data["isGlobalProxyInfo"] = is_global_proxy_info
        if is_ipv6 is not None:
            data["isIpv6"] = is_ipv6
        return self._post("/browser/proxy/update", data)

    def update_proxy_typed(self, request: ProxyUpdateRequest | dict[str, Any]) -> Any:
        return self._post("/browser/proxy/update", self._payload(request))

    def update_remark(self, browser_ids: Sequence[str], remark: str) -> Any:
        return self._post("/browser/remark/update", self._payload(UpdateRemarkRequest(browserIds=list(browser_ids), remark=remark)))

    def check_agent(
        self,
        host: str,
        port: str | int,
        proxy_type: str,
        proxy_user_name: str | None = None,
        proxy_password: str | None = None,
        check_exists: int | None = None,
    ) -> Any:
        data: dict = {"host": host, "port": str(port), "proxyType": proxy_type}
        if proxy_user_name:
            data["proxyUserName"] = proxy_user_name
        if proxy_password:
            data["proxyPassword"] = proxy_password
        if check_exists is not None:
            data["checkExists"] = check_exists
        return self._post("/checkagent", data)

    def check_agent_typed(self, request: CheckAgentRequest | dict[str, Any]) -> Any:
        return self._post("/checkagent", self._payload(request))

    # Local library data (extralog) endpoints
    def extralog_list(
        self,
        page: int,
        page_size: int,
        search_key: str,
        search_value: str,
        order_by: str | None = None,
    ) -> Any:
        data: dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "search_key": search_key,
            "search_value": search_value,
        }
        if order_by is not None:
            data["order_by"] = order_by
        return self._post("/extralog/list", data)

    def extralog_list_typed(
        self, page: int, page_size: int, search_key: str, search_value: str, order_by: str | None = None
    ) -> ExtralogListData:
        data: dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "search_key": search_key,
            "search_value": search_value,
        }
        if order_by is not None:
            data["order_by"] = order_by
        return self._post_typed("/extralog/list", data, ExtralogListData)

    def extralog_add(
        self,
        log_key: str,
        log_name: str,
        log_value: str,
        log_type: str,
        log_desc: str | None = None,
        log_remark: str | None = None,
        log_extra_info: str | None = None,
    ) -> Any:
        data: dict[str, Any] = {
            "log_key": log_key,
            "log_name": log_name,
            "log_value": log_value,
            "log_type": log_type,
        }
        if log_desc is not None:
            data["log_desc"] = log_desc
        if log_remark is not None:
            data["log_remark"] = log_remark
        if log_extra_info is not None:
            data["log_extra_info"] = log_extra_info
        return self._post("/extralog/add", data)

    def extralog_add_typed(self, **fields: Any) -> ExtralogItem:
        return self._post_typed("/extralog/add", fields, ExtralogItem)

    def extralog_update(self, log_id: int | None = None, **fields) -> Any:
        if log_id is None and "id" in fields:
            log_id = fields.pop("id")
        if log_id is None:
            raise ValueError("log_id is required")
        data: dict[str, Any] = {"id": log_id}
        data.update(fields)
        return self._post("/extralog/update", data)

    def extralog_delete(self, log_id: int | None = None, **kwargs: Any) -> Any:
        if log_id is None and "id" in kwargs:
            log_id = kwargs.pop("id")
        if log_id is None:
            raise ValueError("log_id is required")
        return self._post("/extralog/delete", {"id": log_id})

    def extralog_detail(self, log_id: int | None = None, **extra) -> Any:
        if log_id is None and "id" in extra:
            log_id = extra.pop("id")
        if log_id is None:
            raise ValueError("log_id is required")
        data: dict[str, Any] = {"id": log_id}
        data.update(extra)
        return self._post("/extralog/detail", data)

    def extralog_detail_typed(self, log_id: int) -> ExtralogItem:
        return self._post_typed("/extralog/detail", {"id": log_id}, ExtralogItem)

    def extralog_clear(self) -> Any:
        return self._post("/extralog/clear")
