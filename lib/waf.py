import requests
from colorama import Fore
from urllib.parse import parse_qsl, urlparse, urlsplit

"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""

Red = Fore.LIGHTRED_EX
White = Fore.WHITE
Green = Fore.LIGHTGREEN_EX

def waf(url):
    domain = urlparse(url).netloc
    protocol = urlparse(url).scheme
    urle = protocol + "://" + domain + "/"
    r = requests.get(urle + "<script>alert(1)</script>")
    if r.status_code == 403:
        print(f"{Red}WAF detetada {Fore.WHITE}-> {Green}{r.headers['server'].title()} {White}(Possible name of WAF)")
    else:
        pass
    