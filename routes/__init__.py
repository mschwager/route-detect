from importlib.metadata import version

from . import commands  # noqa: F401
from . import rules  # noqa: F401
from . import templates  # noqa: F401


__version__ = version("route-detect")
