from pydantic import BaseModel


class BaseBrowserModel(BaseModel):
    pass


class BrowserFingerprint(BaseBrowserModel):
    id: str
    seq: int
    browserId: str
    ostype: str
    os: str
    version: str
    userAgent: str
    isIpCreateTimeZone: bool
    timeZone: str
    webRTC: str
    position: str
    isIpCreatePosition: bool
    isIpCreateLanguage: bool
    resolutionType: str
    resolution: str
    fontType: str
    canvas: str
    webGL: str
    webGLManufacturer: str
    webGLMeta: str
    webGLRender: str
    audioContext: str
    mediaDevice: str
    clientRects: str
    hardwareConcurrency: str
    deviceMemory: str
    deviceNameType: str
    deviceName: str
    doNotTrack: str
    flash: str
    portScanProtect: str
    portWhiteList: str
    isDelete: int
    colorDepth: int
    devicePixelRatio: float
    createdBy: str
    createdTime: str
    updateBy: str
    updateTime: str


class Browser(BaseBrowserModel):
    id: str
    seq: int
    code: str
    platform: str
    platformIcon: str
    url: str
    name: str
    userName: str
    password: str
    cookie: str
    proxyMethod: int
    proxyType: str
    agentId: str
    host: str
    proxyUserName: str
    proxyPassword: str
    lastIp: str
    lastCountry: str
    country: str
    province: str
    city: str
    remark: str
    status: int
    operUserId: str | None = None
    operUserName: str
    operTime: str
    isDelete: int
    delReason: str
    isMostCommon: int
    tempStr: str | None = None
    createdBy: str
    userId: str
    createdTime: str
    updateBy: str | None = None
    updateTime: str | None = None
    mainUserId: str
    browserFingerPrint: BrowserFingerprint | None = None
    createdName: str
    belongUserName: str | None = None
    updateName: str | None = None
    agentIpCount: int | None = None
    belongToMe: bool
    ip: str
