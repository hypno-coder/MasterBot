from enum import Enum
from cachetools import TTLCache

# Throtling Settings
class SpamConfig(Enum):
    common = 10
    free_menu = 10

def genTrotCash():
    caches: dict[str, TTLCache] = {}
    for item in SpamConfig:
        caches.update({item.name: TTLCache(maxsize=10_000, ttl=item.value)})

    return caches

