# -*- coding: utf-8 -*-
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

