"""
    Standard Python initialiser handling imports from modules and version number
"""
from .pbParse import *

from importlib.metadata import version
try:
    __version__ = version("pybonsai")
except:
    __version__ = ""
print(f"\npybonsai {__version__} by Dr Alan Robinson G1OJS\n\n")


