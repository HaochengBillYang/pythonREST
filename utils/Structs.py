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
    diskTagList: list[str]
    diskSerialNumber: str
