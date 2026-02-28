from enum import Enum


class EnumChroot(Enum):
    FULL = "full"
    MINIMAL = "minimal"

    @staticmethod
    def from_string(s):
        try:
            return EnumCommand[s]
        except KeyError:
            raise ValueError()


class EnumCommand(Enum):
    KERNEL = "kernel"
    ASSETS = "assets"
    BUNDLE = "bundle"

    @staticmethod
    def from_string(s):
        try:
            return EnumCommand[s]
        except KeyError:
            raise ValueError()


class EnumContainerEnvironment(Enum):
    DOCKER = "docker"
    PODMAN = "podman"


class EnumEnvironment(Enum):
    LOCAL = "local"
    DOCKER = "docker"
    PODMAN = "podman"

    @staticmethod
    def from_string(s):
        try:
            return EnumCommand[s]
        except KeyError:
            raise ValueError()


class EnumPackageType(Enum):
    CONAN = "conan"
    SLIM = "slim"
    FULL = "full"

    @staticmethod
    def from_string(s):
        try:
            return EnumCommand[s]
        except KeyError:
            raise ValueError()


class EnumKernelBase(Enum):
    LOS = "los"
    PA = "pa"
    X = "x"
    AOSP = "aosp"

    @staticmethod
    def from_string(s):
        try:
            return EnumCommand[s]
        except KeyError:
            raise ValueError()
