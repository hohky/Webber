import requests
from .common.colors import *

class Method:
    def __init__(self, url):
        self.url = url

    def __put(self):
        self.r = requests.put(self.url + "/dww23d.txt", data="self.data")
        return "PUT" , self.r.status_code

    def __post(self):
        self.r = requests.post(self.url, data="dwwd")
        return "POST" , self.r.status_code

    def __delete(self):
        self.r = requests.delete(self.url)
        return "DELETE" , self.r.status_code

    def __print(self, func):
        return(f"{Green}[{Red}Method{Green}]{Cyanf} {func()}{White}")

    def send(self):
        print(self.__print(self.__post))
        print(self.__print(self.__put))
        print(self.__print(self.__delete))
