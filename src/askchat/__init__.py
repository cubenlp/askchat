"""Top-level package for askchat."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '2.1.0'

from .elements import ChatFileCompletionType
from .utils import show_resp

__all__ = [
    "ChatFileCompletionType",
    "show_resp",
]