import os
import io
import sys
import json
import logging
import argparse
from typing import Any
from pathlib import Path
from importlib.metadata import version

from pydantic.types import PastDate

from zkb.core import KernelBuilder, AssetsCollector
from zkb.tools import cleaning as cm, commands as ccmd, Logger as logger
from zkb.enums import EnumChroot, EnumCommand, EnumEnvironment, EnumContainerEnvironment, EnumKernelBase, EnumPackageType
from zkb.configs import ArgumentConfig, DirectoryConfig as dcfg
from zkb.engines import GenericContainerEngine
from zkb.commands import KernelCommand, AssetsCommand, BundleCommand
from zkb.managers import ResourceManager


def __get_version() -> str:
    """Get app version.

    Version is retrieved depending on the way the app
    is launched (as PIP package or from source).

    :return: App version.
    :rtype: str
    """
    msg = "zero_kernel {}"

    try:
        return msg.format(version("zero-kernel"))
    except Exception:
        with open(Path(__file__).absolute().parents[1] / "pyproject.toml", "r") as f:
            v = f.read().split('version = "')[1].split('"')[0]
        return msg.format(v)


def parse_args() -> argparse.Namespace:
    """Parse the script arguments.

    :return: Namespace of arguments.
    :rtype: argparse.Namespace
    """
    # show the 'help' message if no arguments supplied
    args = None if sys.argv[1:] else ["-h"]

    # parser and subparsers
    parser_parent = argparse.ArgumentParser(description="Advanced Android kernel builder with Kali NetHunter support.")
    subparsers = parser_parent.add_subparsers(dest="command")
    parser_kernel = subparsers.add_parser(EnumCommand.KERNEL.value, help="build the kernel")
    parser_assets = subparsers.add_parser(EnumCommand.ASSETS.value, help="collect assets")
    parser_bundle = subparsers.add_parser(EnumCommand.BUNDLE.value, help="build the kernel + collect assets")

    # main parser arguments
    parser_parent.add_argument(
        "--clean",
        dest="clean_root",
        action="store_true",
        help="clean the root directory"
    )
    parser_parent.add_argument("-v", "--version", action="version", version=__get_version())

    # common arguments
    common_codename = {
        "name_or_flags": ("--codename",),
        "config": {
            "required": True,
            "dest": "codename",
            "type": str,
            "help": "device codename"
        }
    }
    common_benv = {
        "name_or_flags": ("--build-env",),
        "config": {
            "required": True,
            "dest": "benv",
            "type": EnumEnvironment.from_string,
            "choices": tuple(EnumEnvironment),
            "help": "build environment"
        }
    }
    common_base = {
        "name_or_flags": ("--base",),
        "config": {
            "required": True,
            "dest": "base",
            "type": EnumKernelBase.from_string,
            "choices": tuple(EnumKernelBase),
            "help": "kernel source base"
        }
    }
    common_defconfig = {
        "name_or_flags": ("--defconfig",),
        "config": {
            "required": False,
            "dest": "defconfig",
            "type": Path,
            "help": "path to custom defconfig"
        }
    }
    common_lkv = {
        "name_or_flags": ("--lkv",),
        "config": {
            "required": True,
            "dest": "lkv",
            "type": str,
            "help": "Linux kernel version"
        }
    }
    common_ksu = {
        "name_or_flags": ("--ksu",),
        "config": {
            "action": "store_true",
            "dest": "ksu",
            "help": "flag for KernelSU support"
        }
    }
    common_clean_image = {
        "name_or_flags": ("--clean-image",),
        "config": {
            "action": "store_true",
            "dest": "clean_image",
            "help": "clean Docker cache after the build"
        }
    }

    # kernel
    parser_kernel.add_argument(*common_benv["name_or_flags"], **common_benv["config"])
    parser_kernel.add_argument(*common_base["name_or_flags"], **common_base["config"])
    parser_kernel.add_argument(*common_codename["name_or_flags"], **common_codename["config"])
    parser_kernel.add_argument(*common_lkv["name_or_flags"], **common_lkv["config"])
    parser_kernel.add_argument(*common_ksu["name_or_flags"], **common_ksu["config"])
    parser_kernel.add_argument(*common_defconfig["name_or_flags"], **common_defconfig["config"])
    parser_kernel.add_argument(*common_clean_image["name_or_flags"], **common_clean_image["config"])
    parser_kernel.add_argument(
        "-c", "--clean",
        dest="clean_kernel",
        action="store_true",
        help="don't build anything, only clean kernel directories"
    )

    # assets
    parser_assets.add_argument(*common_benv["name_or_flags"], **common_benv["config"])
    parser_assets.add_argument(*common_base["name_or_flags"], **common_base["config"])
    parser_assets.add_argument(*common_codename["name_or_flags"], **common_codename["config"])
    parser_assets.add_argument(*common_ksu["name_or_flags"], **common_ksu["config"])
    parser_assets.add_argument(*common_clean_image["name_or_flags"], **common_clean_image["config"])
    parser_assets.add_argument(
        "--chroot",
        type=str,
        required=True,
        choices=EnumChroot,
        help="select Kali chroot type"
    )
    parser_assets.add_argument(
        "--rom-only",
        dest="rom_only",
        action="store_true",
        help="download only the ROM as an asset"
    )
    parser_assets.add_argument(
        "--clean",
        dest="clean_assets",
        action="store_true",
        help="autoclean 'assets' folder if it exists"
    )

    # bundle
    parser_bundle.add_argument(*common_benv["name_or_flags"], **common_benv["config"])
    parser_bundle.add_argument(*common_base["name_or_flags"], **common_base["config"])
    parser_bundle.add_argument(*common_codename["name_or_flags"], **common_codename["config"])
    parser_bundle.add_argument(*common_lkv["name_or_flags"], **common_lkv["config"])
    parser_bundle.add_argument(*common_ksu["name_or_flags"], **common_ksu["config"])
    parser_bundle.add_argument(*common_defconfig["name_or_flags"], **common_defconfig["config"])
    parser_bundle.add_argument(*common_clean_image["name_or_flags"], **common_clean_image["config"])
    parser_bundle.add_argument(
        "--package-type",
        type=str,
        required=True,
        dest="package_type",
        choices=EnumPackageType,
        help="select package type of the bundle"
    )
    parser_bundle.add_argument(
        "--conan-upload",
        action="store_true",
        dest="conan_upload",
        help="upload Conan packages to remote"
    )
    return parser_parent.parse_args(args)


def main() -> None:
    args = parse_args()
    logger().get_logger()  # type: ignore
    log = logging.getLogger("ZeroKernelLogger")

    # start preparing the environment
    os.chdir(dcfg.root)
    if args.clean_root:
        cm.root()
        sys.exit(0)

    # define env variable with kernel version
    with open(dcfg.root / "pyproject.toml", encoding="utf-8") as f:
        os.environ["KVERSION"] = f.read().split('version = "')[1].split('"')[0]

    # create a config for checking and storing arguments
    if args.command != "assets" and args.defconfig:
        args.defconfig = args.defconfig if args.defconfig.is_absolute() else Path.cwd() / args.defconfig
    arguments = vars(args)
    log.debug(f"Arguments are: {arguments}")

    acfg = ArgumentConfig(**arguments)
    acfg.check_settings()

    # determine the build variation
    match args.benv:
        case EnumContainerEnvironment.DOCKER | EnumContainerEnvironment.PODMAN:
            with GenericContainerEngine(**json.loads(acfg.model_dump_json())) as engined_cmd:
                ccmd.launch(engined_cmd)

        case EnumEnvironment.LOCAL:
            kernel_builder = KernelBuilder(
                codename = args.codename,
                base = args.base,
                lkv = args.lkv,
                clean_kernel = args.clean_kernel,
                ksu = args.ksu,
                defconfig = args.defconfig,
                rmanager = ResourceManager(
                    codename = args.codename,
                    lkv = args.lkv,
                    base = args.base
                )
            )
            assets_collector = AssetsCollector(
                codename = args.codename,
                base = args.base,
                chroot = args.chroot,
                clean_assets = args.clean_assets,
                rom_only = args.rom_only,
                ksu = args.ksu,
            )

            match args.command:
                case EnumCommand.KERNEL:
                    kc = KernelCommand(kernel_builder=kernel_builder)
                    kc.execute()

                case EnumCommand.ASSETS:
                    ac = AssetsCommand(assets_collector=assets_collector)
                    ac.execute()

                case EnumCommand.BUNDLE:
                    bc = BundleCommand(
                        kernel_builder = kernel_builder,
                        assets_collector = assets_collector,
                        package_type = args.package_type,
                        base = args.base
                    )
                    bc.execute()


if __name__ == "__main__":
    # for logs to show in the right order in various build / CI/CD systems
    sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), "wb", 0), write_through=True)
    main()
