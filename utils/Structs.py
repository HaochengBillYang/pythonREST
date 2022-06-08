from typing import Optional

from pydantic import BaseModel


class Volume(BaseModel):
    id: str
    name: Optional[str]
    numericalId: Optional[int]


class Initiator(BaseModel):
    id: str
    iqn: Optional[str]


class DiskInfo(BaseModel):
    diskId: str
    mountPoint: str
    hostId: str
    state: str
    deviceNodeName: str
    diskTagList: list[str]
    diskSerialNumber: str

class HostInfo(BaseModel):
    hostId: str
    hostName: str
    state: str
    clusterId: Optional[str]
    state: str
    allowedToLeaveCluster: bool
