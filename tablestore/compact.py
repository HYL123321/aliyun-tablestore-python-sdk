# -*- coding: utf-8 -*-

"""
兼容Python版本
"""

import sys

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

if is_py2:
    import urlparse
    import httplib

elif is_py3:
    import urllib.parse as urlparse
    import http.client as httplib
