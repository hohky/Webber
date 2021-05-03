import requests
#from bs4 import BeautifulSoup
from colorama import Fore
from urllib.parse import urlparse, urlsplit, parse_qsl
from os import path

"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""
## Colors ##
Green = Fore.GREEN
White = Fore.WHITE
Red = Fore.RED
Yellow = Fore.YELLOW
Redf = Fore.LIGHTRED_EX
Yellowf = Fore.LIGHTYELLOW_EX
Cyan = Fore.CYAN
## Colors ##

dir_path = path.dirname(path.realpath(__file__))

class Vulns:
    
    def __init__(self,url):
        self.url = url
        Vulns.domain = urlparse(self.url).netloc
        Vulns.protocol = urlparse(self.url).scheme
        Vulns.URL = self.url

    def __verify_params(self):
        self.url = Vulns.URL
        params = parse_qsl(urlsplit(self.url).query)
        if len(params) > 0:
            return True
        else:
            return False
    
    def __parser(self):
        self.url = Vulns.URL
        params = parse_qsl(urlsplit(self.url).query)
        return params

    def check_params(self):
        self.url = Vulns.URL
        if self.__verify_params():
            print(f"\n{Redf}Param scanner: {White}")
            self.params = self.__parser()
            #print(f"Parameter(s) found! Total: {len(self.params)}")
            for param in self.params:
                parame = param[0]
                data = param[1]
                self._xss(parame, data)
                self._sqli(parame, data)
        else:
            pass

    def _xss(self, parame, data):
        self.url = Vulns.URL
        self.params = self.__parser()
        self.list = open(dir_path + "/payload/xss.txt")
        self.num = 0
        print(f"[{Green}XSS{White}] Testing GET parameter {Yellowf}({parame}){White}")
        for payload in self.list:
            #count = f"{self.num}/{len(self.list)}"
            self.num += 1
            urle = self.url.replace(data,payload)
            r = requests.get(urle) 
            if r.status_code == 200:
                if payload in r.text:
                    print(f"[{Green}{self.num}{White}] {Yellow}Payload: {Yellowf}{payload.strip()} {White} [{Green}VULNERABLE{White}]")
                else:
                    print(f"[{Green}{self.num}{White}] {Yellow}Payload: {Yellowf}{payload.strip()} {White} [{Red}NOT VULNERABLE{White}]")
            elif r.status_code == 403:
                print(f"[{Red}-{White}] {Redf}Request rejected {White}", end="\r")
            elif self.num == len(self.list):
                print("\n")
            else:
                pass
    
    def _sqli(self, parame, data):
        self.url = Vulns.URL
        self.params = self.__parser()
        #self.list = open(dir_path + "/payload/sqli.txt")
        print(f"\n[{Yellowf}SQLi{White}] Testing GET parameter {Cyan}({parame}){White}")
        self.payload = data + "'"
        urle = self.url.replace(data, self.payload)
        r = requests.get(urle)
        if "mysql_fetch_array" in r.text:
            print(f"[{Yellow}/{White}] {Redf}SQL Error {White} [{Yellow}MAYBE VULNERABLE{White}]\n")
        else:
            print(f"[{Redf}-{White}] {Yellow}MySQL {White} [{Red}NOT VULNERABLE{White}]\n")

