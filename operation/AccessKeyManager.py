import time
from typing import Optional

from pydantic import BaseModel


def extend_timestamp_from_now(extend: int = 0) -> int:
    return int(time.time()) + extend


class AccessKey(BaseModel):
    key: str
    expire_time: int


class AccessKeyManager:
    keys: dict[str, AccessKey] = {}

    @staticmethod
    def findAccessKeyByHost(host: str) -> Optional[AccessKey]:
        key = AccessKeyManager.keys.get(host)
        if key is None:
            return None
        if key.expire_time < extend_timestamp_from_now(0):
            AccessKeyManager.keys.pop(host)
            return None
        return key

    @staticmethod
    def addAccessKey(host: str, key_string: str, key_expire_in: int):
        AccessKeyManager.keys[host] = AccessKey(key=key_string, expire_time=extend_timestamp_from_now(
            key_expire_in - 60
        ))

