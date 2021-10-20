from urllib.parse import parse_qsl, urlparse, urlsplit


"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""


def verify_params(url):
        params = parse_qsl(urlsplit(url).query)
        return if len(params) > 0


def parse_param(url):
    params = parse_qsl(urlsplit().query)
    return params

def parse_url(url):
    parsed = urlparse(url)
    return parsed
