import logging
from typing import Literal

from zkb.core import AssetsCollector
from zkb.tools import banner, fileoperations as fo
from zkb.configs import ModelConfig
from zkb.interfaces import ICommand


log = logging.getLogger("ZeroKernelLogger")


class AssetsCommand(ModelConfig, ICommand):
    """Command responsible for launching the 'assets_collector' core module directly.

    :param zkb.core.AssetsCollector assets_collector: Assets collector object.
    """

    assets_collector: AssetsCollector

    def execute(self) -> None:
        self.assets_collector.run()
