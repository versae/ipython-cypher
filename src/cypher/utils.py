# -*- coding: utf-8 -*-
from collections import namedtuple
import sys


PYTHON_VERSION = sys.version_info
PY2 = sys.version_info[0] == 2

if PY2:
    from cStringIO import StringIO
    from urlparse import urlparse
    text_type = unicode
    string_types = (str, unicode)
else:
    from io import StringIO
    from urllib.parse import urlparse
    text_type = str
    string_types = (str, )

DEFAULT_CONFIGURABLE = {
    "auto_limit": 0,
    "style": 'DEFAULT',
    "short_errors": True,
    "data_contents": True,
    "display_limit": 0,
    "auto_pandas": False,
    "auto_html": False,
    "auto_networkx": False,
    "rest": False,
    "feedback": True,
    "uri": 'http://localhost:7474/db/data/',
}

DefaultConfigurable = namedtuple(
    "DefaultConfigurable",
    ", ".join([k for k in DEFAULT_CONFIGURABLE.keys()])
)

defaults = DefaultConfigurable(**DEFAULT_CONFIGURABLE)
