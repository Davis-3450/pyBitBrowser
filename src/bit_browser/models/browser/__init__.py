from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    pass


class BrowserFingerprint(Base):
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


class BaseBrowserModel(Base):
    """Here we define the minimal fields for the browser"""

    name: str
    remark: str
    proxyMethod: int
    proxyType: str = "noproxy"
    host: str = ""
    port: str = ""
    proxyUserName: str = ""


class Browser(BaseBrowserModel):
    # takes base
    id: str
    seq: int
    code: str
    platform: str
    platformIcon: str
    url: str
    # name: str
    userName: str
    password: str
    cookie: str
    proxyMethod: int
    agentId: str
    proxyPassword: str
    lastIp: str
    lastCountry: str
    country: str
    province: str
    city: str
    status: int
    operUserId: str | None = None
    operUserName: str
    operTime: str | None = None
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


# Creation helper models
class BaseExtraIgnore(BaseModel):
    model_config = ConfigDict(extra="ignore")


class BrowserFingerprintCreate(BaseExtraIgnore):
    coreVersion: str = "112"


class CreateBrowser(BaseBrowserModel):
    browserFingerPrint: BrowserFingerprintCreate
