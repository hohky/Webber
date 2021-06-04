import requests
from .common.colors import *
from .common import parser

"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""

class waf:
    def __init__(self, url):
        self.parsed = parser.parse_url(url)
        self.domain = self.parsed.netloc
        self.protocol = self.parsed.scheme
        self.urle = self.protocol + "://" + self.domain + "/"
        r = requests.get(self.urle + "<script>alert(1)</script>")
        if r.status_code == 403:
            try:
                print(f"{Red}WAF detetada {Fore.WHITE}-> {Green}{r.headers['server'].title()} {White}(Possible name of WAF)")
            except KeyError:
                pass
        else:
            pass
    