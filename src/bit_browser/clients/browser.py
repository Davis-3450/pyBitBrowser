import json

import requests
from constants import HEADERS, URL

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档


class BrowserClient:
    def __init__(self):
        self.url = URL
        self.headers = HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _post(self, endpoint: str, data: dict) -> dict:
        """POST helper method."""
        url = f"{self.url}{endpoint}"
        response = self.session.post(url, data=json.dumps(data))
        return response.json()

    def create_browser(
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
        self, id
    ):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
        data = {"id": f"{id}"}
        r = self._post("/browser/open", data)
        return r

    def close_browser(self, id):  # 关闭窗口
        data = {"id": f"{id}"}
        r = self._post("/browser/close", data)
        return r

    def delete_browser(self, id):  # 删除窗口
        data = {"id": f"{id}"}
        r = self._post("/browser/delete", data)
        return r

    def get_browser_details(self, id):
        data = {"id": f"{id}"}
        r = self._post("/browser/get", data)
        return r

    def reset_closed_state(self, id):
        data = {"id": f"{id}"}
        r = self._post("/users", data)
        return r
