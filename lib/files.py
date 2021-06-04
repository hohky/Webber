import requests
import json
from os import path
from requests.exceptions import ConnectionError
from .common.colors import *
from .common import parser
from time import sleep


"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""



class Fuzz:
    domain = None
    URL = None
    def __init__(self,url):
        self.url = url
        self.parsed = parser.parse_url(self.url)
        Fuzz.domain = self.parsed.netloc
        Fuzz.protocol = self.parsed.scheme
        Fuzz.URL = self.url

    def check(self):
        dir_path = path.dirname(path.realpath(__file__))
        self.list = open(dir_path + "/payload/files.txt")
        print(f"\n{Redf}Fuzzer: {White}")
        self.domain = Fuzz.domain
        self.protocol = Fuzz.protocol
        for item in self.list:
            item = item.strip()
            self.url = self.protocol + "://" + self.domain + "/" + item
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
            try:
                self.r = requests.get(self.url, headers=self.headers)
                if self.r.status_code == 200:
                    try:
                        if self.r.headers['Location'] == self.url:
                            print(f"[{Green}+{White}] {Yellow}{item}{White} [{Green}Redirect Reflected{White}]")
                        elif self.r.headers['Location'] == item:
                            print(f"[{Green}+{White}] {Yellow}{item}{White} [{Green}Redirect Reflected{White}]")
                        else:
                            print(f"[{Yellowf}->{White}] {Yellow}{item}{White} [{Yellowf}Redirect{White}]")
                    except KeyError:
                        print(f"[{Green}+{White}] {Yellow}{item}{White} [{Green}found{White}]")
                elif self.r.status_code == 403:
                    print(f"[{Red}-{White}] {Yellow}{item} {White}[{Redf}Forbidden{White}]")
                elif self.r.status_code == 301:
                    print(f"[{Yellowf}->{White}] {Yellow}{item}{White} [{Yellowf}Redirect{White}]")
                elif self.r.status_code == 302:
                    print(f"[{Yellowf}->{White}] {Yellow}{item}{White} [{Yellowf}Redirect{White}]")
                else:
                    print(f"[{Red}-{White}] {Yellow}{item} {White}[{Red}Not found{White}]", end="\r")
            except ConnectionError:
                pass

    def __bypass(self):
        dir_path = path.dirname(path.realpath(__file__))
        self.url = Fuzz.URL
        f = dir_path + "/payload/headers.txt"
        for header in f:
            header = json.loads(header)
            self.r = requests.get(self.url, headers=header)
            if self.r.status_code == 403:
                print(f"[{Red}-{White}] {Redf}Forbidden - Status_code: {Yellow}{self.r.status_code} {White}", end="\r")
            elif self.r.ok:
                print(f"[{Green}+{White}] OK - Header: {Yellow} {header[0]} {White}")

    def check_ok(self):
        r = requests.get(Fuzz.URL)
        code = r.status_code
        if code == 403:
            print(Yellow, "\nBypass 403 using headers:")
            self.__bypass()
        else:
            pass


