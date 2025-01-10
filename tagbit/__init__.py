"""
Homemade python API for reading NFC NTAG-21X tags.

Originally created to make dumps of Amiibos and
automate writing to NDEF tags.

Tested with and built for the Sony PaSoRi RC-S300 reader. (Since nfcpy doesn't support it)

Created by Akito Hoshi, 2025.
"""

from .reader import *
from .handlers import *
from .utils import *
from .status import *

__all__ = [
    'from_notation',
    'to_notation',
    'ndef_load',
    'ndef_dump',
    'find_page',
    'Reader',
    'NoTagError',
    'TagStatusError',
    'raise_for_status',
    'TagIO',
    'AmiiboHandler',
    'NDEFHandler',
]
