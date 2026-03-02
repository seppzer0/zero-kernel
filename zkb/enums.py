from enum import Enum


class EnumChroot(Enum):
    FULL = "full"
    MINIMAL = "minimal"

    def __str__(self):
        return self.value


class EnumCommand(Enum):
    KERNEL = "kernel"
    ASSETS = "assets"
    BUNDLE = "bundle"

    def __str__(self):
        return self.value


class EnumEnvironment(Enum):
    LOCAL = "local"
    DOCKER = "docker"
    PODMAN = "podman"

    def __str__(self):
        return self.value


class EnumPackageType(Enum):
    CONAN = "conan"
    SLIM = "slim"
    FULL = "full"

    def __str__(self):
        return self.value


class EnumKernelBase(Enum):
    LOS = "los"
    PA = "pa"
    X = "x"
    AOSP = "aosp"

    def __str__(self):
        return self.value
