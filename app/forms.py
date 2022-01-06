from pydantic import BaseModel
from typing import Optional


class EventData(BaseModel):
    eventType: Optional[str] = None
    first_time_login: Optional[int] = None
    time_since_start: Optional[int] = None
    value: Optional[int] = None
    platformAccountId: Optional[int] = None

class DeviceInfo(BaseModel):
    thirdPartyTrackingEnabled: Optional[int] = None
    ifa: Optional[str] = None
    appTrackingTransparencyStatus: Optional[str] = None
    ifaEnabled: Optional[int] = None

class Data(BaseModel):
    eventData: Optional[EventData] = None
    deviceInfo: Optional[DeviceInfo] = None

    eventName: Optional[str] = None
    deviceModel: Optional[str] = None
    osVersion: Optional[str] = None
    screenResolution: Optional[str] = None
    bundleId: Optional[str] = None
    appStore: Optional[str] = None
    appStoreId: Optional[str] = None
    deviceBrand: Optional[str] = None
    deviceCarrier: Optional[str] = None
    deviceIdiom: Optional[str] = None
    processorType: Optional[str] = None
    osInfo: Optional[str] = None
    geoIp: Optional[str] = None

class Event(BaseModel):
    data: Optional[Data] = None

    appUserId: Optional[str] = None
    eventType: Optional[str] = None
    sessionId: Optional[int] = None
    playSessionId: Optional[int] = None
    platform: Optional[str] = None
    appVersion: Optional[str] = None
    ip: Optional[str] = None
    languageCode: Optional[str] = None
    clientTimezoneOffset: Optional[int] = None
    raveId: Optional[str] = None
    environment: Optional[str] = None
    appName: Optional[str] = None
    timestampClient: Optional[int] = None
    clientEventId: Optional[str] = None
    bfgSdkVersion: Optional[str] = None
    bfgudid: Optional[str] = None
    timestampServer: Optional[str] = None
    appBuildVersion: Optional[str] = None
    msgPayloadVersion: Optional[str] = None
    countryCode: Optional[str] = None
