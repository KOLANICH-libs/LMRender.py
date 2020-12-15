import typing
from collections import defaultdict
from enum import Enum
from itertools import product
from os import geteuid
from pathlib import Path, PurePath

from .backends import initDefaultRenderer
from .core import *

__all__ = ("SF", "SF", "isSourceUnavailable", "render")

_isRoot = geteuid() == 0  # we can try to disable the potentially dangerous capabilities if running as root

DEFAULT_RENDERER = initDefaultRenderer()
