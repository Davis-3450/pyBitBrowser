from typing import Optional, Sequence, Any

import requests

from bit_browser.constants import HEADERS, URL
from bit_browser.errors import BadRequest, ValidationError
from bit_browser.models.client import APIResponse
from bit_browser.models.browser import (
    CreateBrowser,
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
        self, endpoint: str, data: dict | None = None, timeout: float | None = 10.0
    ):
        """POST helper that sends JSON and returns parsed JSON.

        Uses `json=` for proper JSON serialization and a default timeout.
        """
        url = f"{self.url}{endpoint}"
        response = self.session.post(url, json=(data or {}), timeout=timeout)

        try:
            r = response
            r.raise_for_status()
            j = r.json()
            v = APIResponse.model_validate(j)
            if r.ok and v.success:
                return v.data
            else:
                raise BadRequest(v.msg)
        except Exception as e:
            raise ValidationError(f"Response validation error: {e}")

    def create_or_update_browser(
        self,
        id: str | None = None,
        name: str,
        remark: str,
        proxy_method: int,
        proxy_type: str = "noproxy",
        host: str = "",
        port: str = "",
        proxy_user_name: str = "",
        core_version: str = "112",
        browser_fingerprint: dict | None = None,
        extra: dict | None = None,
    ):
        """Create or update a browser profile using /browser/update.

        This endpoint is multi-propósito: si se envía `id`, actualiza; si no,
        crea. Se permiten campos adicionales vía `extra` según bitbrowser.md.
        """

        # Base payload following docs and examples
        data = {
            **({"id": id} if id else {}),
            "name": name,  # 窗口名称
            "remark": remark,  # 备注
            "proxyMethod": proxy_method,  # 代理方式 2自定义 3 提取IP
            # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
            "proxyType": proxy_type,
            "host": host,  # 代理主机
            "port": port,  # 代理端口
            "proxyUserName": proxy_user_name,  # 代理账号
            "browserFingerPrint": (
                browser_fingerprint
                if browser_fingerprint is not None
                else {
                    # 指纹对象: 内核版本 112 | 104
                    "coreVersion": core_version,
                }
            ),
        }
        if extra:
            data.update(extra)

        return self._post("/browser/update", data)

    def create_browser(self, payload: CreateBrowser | dict[str, Any]):
        """Create a browser profile using a typed model or a raw dict.

        Accepts `CreateBrowser` (preferred) or a raw dict compatible with
        the `/browser/update` endpoint. This method always creates (no id).
        """
        if isinstance(payload, CreateBrowser):
            data = payload.model_dump()
        else:
            # Ensure no id is passed for creation semantics
            data = {k: v for k, v in payload.items() if k != "id"}
        return self._post("/browser/update", data)

    # Backwards-compat alias; prefer `create_browser`
    def _edit_browser(
        self,
        id: str | None = None,
        name: str,
        remark: str,
        proxy_method: int,
        proxy_type: str = "noproxy",
        host: str = "",
        port: str = "",
        proxy_user_name: str = "",
        core_version: str = "112",
        browser_fingerprint: dict | None = None,
        extra: dict | None = None,
    ):
        # Maintained for backwards-compat, use create_or_update_browser
        return self.create_or_update_browser(
            id=id,
            name=name,
            remark=remark,
            proxy_method=proxy_method,
            proxy_type=proxy_type,
            host=host,
            port=port,
            proxy_user_name=proxy_user_name,
            core_version=core_version,
            browser_fingerprint=browser_fingerprint,
            extra=extra,
        )

    def update_browsers(self, ids: list[str], remark: str):
        # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
        data = {
            "ids": ids,
            "remark": remark,
            "browserFingerPrint": {},
        }

        # Example:
        # json_data = {
        #     "ids": ["93672cf112a044f08b653cab691216f0"],
        #     "remark": "我是一个备注",
        #     "browserFingerPrint": {},
        # }

        r = self._post("/browser/update/partial", data)

        return r

    def update_browser_partial(self, ids: Sequence[str], **fields):
        """Partial update for one or many browsers via `/browser/update/partial`.

        Pass only the fields you want to modify. For example:
        update_browser_partial([id], name="New Name", browserFingerPrint={})
        """
        data = {"ids": list(ids)}
        data.update(fields)
        return self._post("/browser/update/partial", data)

    def open_browser(
        self, id, args: list[str] | None = None, queue: bool | None = None
    ):
        # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
        data: dict = {"id": f"{id}"}
        if args is not None:
            data["args"] = args
        if queue is not None:
            data["queue"] = queue
        r = self._post("/browser/open", data)
        return r

    def close_browser(self, id):  # 关闭窗口
        data = {"id": f"{id}"}
        return self._post("/browser/close", data)

    def delete_browser(self, id):  # 删除窗口
        data = {"id": f"{id}"}
        return self._post("/browser/delete", data)

    def get_browser_details(self, id):
        data = {"id": f"{id}"}
        return self._post("/browser/detail", data)

    def reset_closed_state(self, id):
        data = {"id": f"{id}"}
        return self._post("/users", data)

    # Additional documented endpoints
    def list_browsers(self, page: int = 0, page_size: int = 100, **filters):
        data = {"page": page, "pageSize": page_size}
        data.update(filters)
        return self._post("/browser/list", data)

    def windowbounds_reset(self, **window_bounds):
        # type, startX, startY, width, height, col, spaceX, spaceY, offsetX, offsetY
        return self._post("/windowbounds", window_bounds)

    def windowbounds_flexible(self, seqlist: Sequence[int] | None = None):
        data: dict[str, Any] = {}
        if seqlist is not None:
            data["seqlist"] = list(seqlist)
        return self._post("/windowbounds/flexable", data)

    def get_all_displays(self):
        return self._post("/alldisplays")

    def rpa_run(self, task_id: str):
        return self._post("/rpa/run", {"id": task_id})

    def rpa_stop(self, task_id: str):
        return self._post("/rpa/stop", {"id": task_id})

    def autopaste(self, browser_id: str, url: str):
        return self._post("/autopaste", {"browserId": browser_id, "url": url})

    def utils_read_excel(self, filepath: str):
        return self._post("/utils/readexcel", {"filepath": filepath})

    def utils_read_file(self, filepath: str):
        return self._post("/utils/readfile", {"filepath": filepath})

    def cookies_set(self, browser_id: str, cookies: list[dict]):
        return self._post(
            "/browser/cookies/set", {"browserId": browser_id, "cookies": cookies}
        )

    def cookies_get(self, browser_id: str):
        return self._post("/browser/cookies/get", {"browserId": browser_id})

    def cookies_clear(self, browser_id: str, save_synced: bool = True):
        return self._post(
            "/browser/cookies/clear",
            {"browserId": browser_id, "saveSynced": save_synced},
        )

    def cookies_format(self, cookie: str | list[dict], hostname: str | None = None):
        data = {"cookie": cookie}
        if hostname is not None:
            data["hostname"] = hostname
        return self._post("/browser/cookies/format", data)

    def fingerprint_random(self, browser_id: str):
        return self._post("/browser/fingerprint/random", {"browserId": browser_id})

    def clear_cache(self, ids: list[str]):
        return self._post("/cache/clear", {"ids": ids})

    def clear_cache_except_extensions(self, ids: list[str]):
        return self._post("/cache/clear/exceptExtensions", {"ids": ids})

    def get_opened_ports(self):
        return self._post("/browser/ports")

    def get_all_pids(self):
        return self._post("/browser/pids/all")

    def get_pids(self, ids: Sequence[str]):
        return self._post("/browser/pids", {"ids": list(ids)})

    def delete_browsers_by_ids(self, ids: list[str]):
        return self._post("/browser/delete/ids", {"ids": ids})

    def close_by_seqs(self, seqs: Sequence[int]):
        return self._post("/browser/close/byseqs", {"seqs": list(seqs)})

    def close_all(self):
        return self._post("/browser/close/all")

    def update_group(self, group_id: str, browser_ids: Sequence[str]):
        return self._post(
            "/browser/group/update",
            {"groupId": group_id, "browserIds": list(browser_ids)},
        )

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
    ):
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

    def update_remark(self, browser_ids: Sequence[str], remark: str):
        return self._post(
            "/browser/remark/update", {"browserIds": list(browser_ids), "remark": remark}
        )

    def check_agent(
        self,
        host: str,
        port: str | int,
        proxy_type: str,
        proxy_user_name: str | None = None,
        proxy_password: str | None = None,
        check_exists: int | None = None,
    ):
        data: dict = {"host": host, "port": str(port), "proxyType": proxy_type}
        if proxy_user_name:
            data["proxyUserName"] = proxy_user_name
        if proxy_password:
            data["proxyPassword"] = proxy_password
        if check_exists is not None:
            data["checkExists"] = check_exists
        return self._post("/checkagent", data)

    # Local library data (extralog) endpoints
    def extralog_list(
        self,
        page: int,
        page_size: int,
        search_key: str,
        search_value: str,
        order_by: str | None = None,
    ):
        data: dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "search_key": search_key,
            "search_value": search_value,
        }
        if order_by is not None:
            data["order_by"] = order_by
        return self._post("/extralog/list", data)

    def extralog_add(
        self,
        log_key: str,
        log_name: str,
        log_value: str,
        log_type: str,
        log_desc: str | None = None,
        log_remark: str | None = None,
        log_extra_info: str | None = None,
    ):
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

    def extralog_update(self, id: int, **fields):
        data: dict[str, Any] = {"id": id}
        data.update(fields)
        return self._post("/extralog/update", data)

    def extralog_delete(self, id: int):
        return self._post("/extralog/delete", {"id": id})

    def extralog_detail(self, id: int, **extra):
        data: dict[str, Any] = {"id": id}
        data.update(extra)
        return self._post("/extralog/detail", data)

    def extralog_clear(self):
        return self._post("/extralog/clear")
