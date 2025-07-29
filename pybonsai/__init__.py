"""
    Standard Python initialiser handling imports from modules and version number
"""
from .pyparse import doc_object_tree

from importlib.metadata import version
try:
    __version__ = version("necbol")
except:
    __version__ = ""
print(f"\npybonsai V{__version__} by Dr Alan Robinson G1OJS\n\n")
