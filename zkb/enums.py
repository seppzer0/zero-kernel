from enum import Enum


class EnumChroot(str, Enum):
    FULL = "full"
    MINIMAL = "minimal"

    def __str__(self):
        return self.value


class EnumCommand(str, Enum):
    KERNEL = "kernel"
    ASSETS = "assets"
    BUNDLE = "bundle"

    def __str__(self):
        return self.value


class EnumContainerEnvironment(Enum):
    DOCKER = "docker"
    PODMAN = "podman"


class EnumEnvironment(str, Enum):
    LOCAL = "local"
    DOCKER = "docker"
    PODMAN = "podman"

    def __str__(self):
        return self.value


class EnumPackageType(str, Enum):
    CONAN = "conan"
    SLIM = "slim"
    FULL = "full"

    def __str__(self):
        return self.value


class EnumKernelBase(str, Enum):
    LOS = "los"
    PA = "pa"
    X = "x"
    AOSP = "aosp"

    def __str__(self):
        return self.value
