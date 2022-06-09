import uuid
from uuid import UUID

from pydantic import BaseModel


class Config(BaseModel):
    config_id: str = str(uuid.uuid4())
    pass


### Connection
class ConnectionConfig(Config):
    host: str
    port: int

### Host


class DiskAction:
    tags: list[str]


class HostConfig(Config):
    host: str
    actionsOnDisks: list[DiskAction]
    defaultAction: DiskAction




### Cluster
