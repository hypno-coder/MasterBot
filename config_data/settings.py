from enum import Enum
from cachetools import TTLCache

# Throtling Settings
class SpamConfig(Enum):
    # menu
    main_menu = 2
    paid_menu = 2
    free_menu = 2
    jantra_menu = 2
    code_menu = 2
    calendar_menu = 4
    horoscope_menu = 2

    #conversations
    sonnik_conv = 2

    common = 4

def genTrotCash():
    caches: dict[str, TTLCache] = {}
    for item in SpamConfig:
        caches.update({item.name: TTLCache(maxsize=10_000, ttl=item.value)})

    return caches

