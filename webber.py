# Made by HooS
import requests
import argparse
import time
import sys
import ctypes
from requests.exceptions import ConnectionError
from requests.exceptions import MissingSchema
from colorama import Fore
## My functions
from lib.files import Fuzz

## Colors ##
Green = Fore.GREEN
White = Fore.WHITE
Red = Fore.RED
Cyan = Fore.CYAN
Blue = Fore.BLUE
Magentaf = Fore.LIGHTMAGENTA_EX
Redf = Fore.LIGHTRED_EX
## Colors ##

try:
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except AttributeError:
    pass

__version__ = 1.2
__author__ = 'HooS'

parser = argparse.ArgumentParser(description="Scan webpage for searching vulnerability!")
parser.add_argument("-u", "--url", help="Indicar o URL")
parser.add_argument("-v", "--version", help="Indicate the version of this tool'", action="store_true")
parser.add_argument("--skip-rate", help="Skip the Rate limiting", action="store_true")
parser.add_argument("--update", help="Update the tool",action="store_true")
args = parser.parse_args()

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

def banner():
    print(f'''{Cyan} __      __   _    _             
 \ \    / /__| |__| |__  ___ _ _ 
  \ \/\/ / -_) '_ \ '_ \/ -_) '_|
   \_/\_/\___|_.__/_.__/\___|_|  
                                 {White}''')

def rate_limiting(url):
    print("Send multiple HTTP requests... Verify the rate limiting is exists...")
    for send in range(20):
        response = requests.get(url)
    if response.ok:
        print(f"[{Green}+{White}] RATE LIMITING [{Green}VULNERABLE{White}]")
    else:
        print(f"[{Red}-{White}] RATE LIMITING [{Red}NOT VULNERABLE{White}]")
        for by in range(15):
            bypass = requests.get(url, headers={"X-Forwarded-For": "127.0.0.1"})
        if bypass.ok:
            print(f"[{Green}+{White}] RATE LIMITING BYPASS [{Green}VULNERABLE{White}] - with Header 'X-Forwarded-For'")
        else:
            print(f"[{Red}-{White}]RATE LIMITING BYPASS [{Red}NOT VULNERABLE{White}]")
def verify(url):
    pedido = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
    req = pedido.headers
    ## Verificar se tem o header Server
    try:
        print("Server: ",Magentaf, req['Server'], White)
    except KeyError:
        print("Server header [NOT EXIST]")

    ## Verificar se tem o header X-XSS-Protecion
    try:
        if req['X-XSS-Protection'] == "0":
            print(f"[{Green}+{White}] XSS protection [{Green}VULNERABLE{White}]")
        elif req['X-XSS-Protection'] == "1":
            print(f"[{Red}-{White}] XSS protection [{Red}NOT VULNERABLE{White}]")
        elif req['X-XSS-Protection'] == "1; mode=block":
            print(f"[{Red}-{White}] XSS protection [{Red}NOT VULNERABLE{White}]")
        else:
            print(f"[{Red}-{White}] XSS protection [{Red}NOT VULNERABLE{White}] - ", req['X-XSS-Protection'])
    except KeyError:
        print(f"[{Green}+{White}] XSS protection [{Green}VULNERABLE{White}] (not exist header!)")
    ## Verificar se é vulneravel a Clickjacking
    try:
        if req['X-Frame-Options'] == "SAMEORIGIN":
            print(f"[{Red}-{White}] Clickjacking [{Red}NOT VULNERABLE{White}]")
        else:
            print(f"[{Red}-{White}] Clickjacking [{Red}NOT VULNERABLE{White}]")
    except KeyError:
        print(f"[{Green}+{White}] Clickjacking [{Green}VULNERABLE{White}]")

try:
    if args.url:
        fz = Fuzz(args.url)
        banner()
        print("URL: ",Blue, args.url, White)
        verify(args.url)
        if not args.skip_rate:
           rate_limiting(args.url)
        fz.check()
    elif args.version:
        banner()
        print("Developed by", __author__)
        print(f"Version of tool:{Green}", __version__,White)
    elif args.update:
        ## Verify updates in repository github
        reqs = requests.get("https://raw.githubusercontent.com/hohky/Webber/main/options.json")
        options = reqs.json()
        banner()
        if options['version'] == __version__:
            print("The tool is up to date!")
        else:
            print(f"New Version: {options['version']} \n Update in https://github.com/hohky/Webber")
    else:
        banner()
        print("\nHelp command -> --help")
except ConnectionError:
    banner()
    print("\r ({}) Connection error!" .format(time.strftime("%X")))
    
except KeyboardInterrupt:
    banner()
    print("\r({}{}{}) Action canceled by user!" .format(Redf,time.strftime("%X"), White))

except MissingSchema:
    banner()
    print("\r({}) Invalid URL!" .format(time.strftime("%X")))

## Verify version of Python
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

if __name__ != '__main__':
    sys.exit()
