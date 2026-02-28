from pathlib import Path
from pydantic.dataclasses import dataclass

from zkb.enums import EnumCommand


@dataclass
class DirectoryConfig:
    """Config for key directory paths."""
    root: Path = Path(__file__).absolute().parents[2]
    kernel: Path = root / EnumCommand.KERNEL.value
    assets: Path = root / EnumCommand.ASSETS.value
    bundle: Path = root / EnumCommand.BUNDLE.value
