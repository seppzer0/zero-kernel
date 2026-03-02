from typing import override

from zkb.enums import EnumKernelBase
from zkb.clients.rom_api import RomApiClient


class ParanoidAndroidApiClient(RomApiClient):
    """Client for limited interaction with ParanoidAndroid API."""

    endpoint: str = "https://api.paranoidandroid.co/updates/{}"
    json_key: str = "updates"
    rom_name: EnumKernelBase = EnumKernelBase.PA

    @override
    def map_codename(self) -> str:
        # specific rules for PA's API
        specials = {
            "dumpling": "oneplus5t",
            "cheeseburger": "oneplus5",
        }
        return specials[self.codename] if self.codename in specials else self.codename
