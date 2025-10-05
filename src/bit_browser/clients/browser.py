import json
from typing import Optional

import requests

from bit_browser.constants import HEADERS, URL
from bit_browser.errors import BadRequest, ValidationError
from bit_browser.models.client import APIResponse

# 官方文档地址
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

    def _post(self, endpoint: str, data: dict | None = None):
        """POST helper that sends JSON and returns parsed JSON."""
        url = f"{self.url}{endpoint}"
        response = self.session.post(url, data=json.dumps(data or {}))

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

    def _edit_browser(
        self,
        browser: str,
        remark: str,
        proxy_method: int,
        proxy_type: str = "noproxy",
        host: str = "",
        port: str = "",
        proxy_user_name: str = "",
        core_version: str = "112",
    ) -> str:
        # TODO: change to use pydantic model - improve validations
        data = {
            "name": browser,  # 窗口名称
            "remark": remark,  # 备注
            "proxyMethod": proxy_method,  # 代理方式 2自定义 3 提取IP
            # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
            "proxyType": proxy_type,
            "host": host,  # 代理主机
            "port": port,  # 代理端口
            "proxyUserName": proxy_user_name,  # 代理账号
            "browserFingerPrint": {  # 指纹对象
                "coreVersion": core_version  # 内核版本 112 | 104，建议使用112，注意，win7/win8/winserver 2012 已经不支持112内核了，无法打开
            },
        }
        # Example:
        #  json_data = {
        #     "name": "google",  # 窗口名称
        #     "remark": "",  # 备注
        #     "proxyMethod": 2,  # 代理方式 2自定义 3 提取IP
        #     # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
        #     "proxyType": "noproxy",
        #     "host": "",  # 代理主机
        #     "port": "",  # 代理端口
        #     "proxyUserName": "",  # 代理账号
        #     "browserFingerPrint": {  # 指纹对象
        #         "coreVersion": "112"  # 内核版本 112 | 104，建议使用112，注意，win7/win8/winserver 2012 已经不支持112内核了，无法打开
        #     },
        # }

        res = self._post("/browser/update", data)
        browser_id = res["data"]["id"]
        print(browser_id)
        return browser_id

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

    def cookies_format(self, cookie, hostname: str | None = None):
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

    def delete_browsers_by_ids(self, ids: list[str]):
        return self._post("/browser/delete/ids", {"ids": ids})

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
