import requests
from os import path
from requests.exceptions import ConnectionError
from urllib.parse import urlparse
from colorama import Fore

## Colors ##
Green = Fore.GREEN
White = Fore.WHITE
Red = Fore.RED
Yellow = Fore.YELLOW
Redf = Fore.LIGHTRED_EX
## Colors ##

class Fuzz:
    domain = None
    def __init__(self,url):
        self.url = url
        Fuzz.domain = urlparse(self.url).netloc

    def check(self):
        dir_path = path.dirname(path.realpath(__file__))
        self.list = open(dir_path+ "/payload/files.txt")
        print(f"\n{Redf}Fuzzer: {White}")
        for item in self.list:
            item = item.strip()
            self.url = "https://" + Fuzz.domain + "/" + item
            try:
                self.r = requests.get(self.url)
                if self.r.ok:
                    print(f"[{Red}-{White}] {Yellow}{item} [{Green}found{White}]")
                elif self.r.status_code == 403:
                    print(f"[{Red}-{White}] {Yellow}{item} [{Redf}Forbidden{White}]")
                else:
                    print(f"[{Red}-{White}] {Yellow}{item} [{Red}Not found{White}]", end="\r")
            except ConnectionError:
                pass


   # def __bypass(self, path):
