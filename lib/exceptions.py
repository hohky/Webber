
"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""


class Error(Exception):
    pass


class NotFoundParams(Error):
    # Not find query string in url
    pass

class VersionOutdated(Error):
    # Needs to use python3
    exit