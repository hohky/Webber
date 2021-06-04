import requests
#from bs4 import BeautifulSoup
from .common.colors import *
from .common import parser
from os import path

"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""

dir_path = path.dirname(path.realpath(__file__))

class Vulns:
    
    def __init__(self,url):
        self.url = url
        self.parsed = parser.parse_url(url)
        Vulns.domain = self.parsed.netloc
        Vulns.protocol = self.parsed.params
        Vulns.URL = self.url
    

    def check_params(self):
        self.url = Vulns.URL
        self.number = 0
        if parser.verify_params(self.url):
            print(f"\n{Redf}Param scanner: {White}")
            self.p = parser.parse_param(self.url)
            self.params = self.p
            #print(f"Parameter(s) found! Total: {len(self.params)}")
            for param in self.params:
                parame = param[0]
                data = param[1]
                self.number += 1
                print(f"\n{Green}-------> {Cyanf}Param #{self.number}\n")
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
                continue
            else:
                pass
    
    def _sqli(self, parame, data):
        self.url = Vulns.URL
        #self.list = open(dir_path + "/payload/sqli.txt")
        print(f"[{Yellowf}SQLi{White}] Testing GET parameter {Cyan}({parame}){White}")
        self.payload = data + "'"
        urle = self.url.replace(data, self.payload)
        r = requests.get(urle)
        if "mysql_fetch_array" in r.text:
            print(f"[{Yellow}/{White}] {Redf}MySQL {White} [{Yellow}MAYBE VULNERABLE{White}]\n")
        elif "sql error" in (r.text).lower():
            print(f"[{Yellow}/{White}] {Redf}SQL Error {White} [{Yellow}MAYBE VULNERABLE{White}]\n")
        else:
            print(f"[{Redf}-{White}] {Yellow}MySQL {White} [{Red}NOT VULNERABLE{White}]\n")
