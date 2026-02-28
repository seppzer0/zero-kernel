import sys
import json
import logging
import platform
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from zkb.enums import EnumEnvironment, EnumCommand, EnumPackageType
from zkb.tools import commands as ccmd


log = logging.getLogger("ZeroKernelLogger")


class ArgumentConfig(BaseModel):
    """Variable storage for usage across the app.

    Only model not using shared ModelConfig.

    :param zkb.enums.EnumEnvironment benv: Build environment.
    :param zkb.enums.EnumCommand command: Builder command to be launched.
    :param str codename: Device codename.
    :param str base: Kernel source base.
    :param str lkv: Linux kernel version.
    :param typing.Optional[str]=None chroot: Chroot type.
    :param typing.Optional[str]=None package_type: Package type.
    :param typing.Optional[bool]=False clean_kernel: Flag to clean folder with kernel sources.
    :param typing.Optional[bool]=False clean_assets: Flag to clean folder for assets storage.
    :param typing.Optional[bool]=False clean_image: Flag to clean a Docker/Podman image from local cache.
    :param typing.Optional[bool]=False rom_only: Flag indicating ROM-only asset collection.
    :param typing.Optional[bool]=False conan_upload: Flag to enable Conan upload.
    :param typing.Optional[bool]=False ksu: Flag indicating KernelSU support.
    :param typing.Optional[Path]=None defconfig: Path to custom defconfig.
    """

    benv: EnumEnvironment
    command: EnumCommand
    codename: str
    base: str
    lkv: Optional[str] = None
    chroot: Optional[str] = None
    package_type: Optional[EnumPackageType] = None
    clean_kernel: Optional[bool] = False
    clean_assets: Optional[bool] = False
    clean_image: Optional[bool] = False
    rom_only: Optional[bool] = False
    conan_upload: Optional[bool] = False
    ksu: Optional[bool] = False
    defconfig: Optional[Path] = None

    def check_settings(self) -> None:
        """Run settings validations.

        :return: None
        """
        # allow only asset colletion on a non-Linux machine
        if self.benv == EnumEnvironment.LOCAL and self.command in {EnumCommand.KERNEL, EnumCommand.BUNDLE}:
            if not platform.system() == "Linux":
                log.error("Can't build kernel on a non-Linux machine.")
                sys.exit(1)
            else:
                # check that it is Debian-based
                try:
                    ccmd.launch("apt --version", loglvl="quiet")
                except Exception:
                    log.error("Detected Linux distribution is not Debian-based.")
                    sys.exit(1)

        # check if specified device is supported
        with open(
            Path(__file__).absolute().parents[2] / "zkb" / "manifests" / "devices.json", encoding="utf-8"
        ) as f:
            devices = json.load(f)

        if self.codename not in devices.keys():
            log.error("Unsupported device codename specified.")
            sys.exit(1)
        if self.command == EnumCommand.BUNDLE:
            # check Conan-related argument usage
            if self.package_type != EnumPackageType.CONAN and self.conan_upload:
                log.error("Cannot use Conan-related arguments with non-Conan packaging\n")
                sys.exit(1)

        # check that the provided defconfig file is valid
        if self.defconfig and not self.defconfig.is_file():
            log.error("Provided path to defconfig is invalid.")
            sys.exit(1)
