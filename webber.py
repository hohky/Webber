# Made by HooS
import requests
import argparse
import time
import sys
import ctypes
from requests.exceptions import ConnectionError
from requests.exceptions import MissingSchema

try:
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except AttributeError:
    print("\n")

__version__ = 1.0
__author__ = 'HooS'

parser = argparse.ArgumentParser(description="Scan webpage for searching vulnerability!")
parser.add_argument("-u", "--url", help="Indicar o URL")
parser.add_argument("-v", "--version", help="Indicate the version of this tool'", action="store_true")
parser.add_argument("--update", help="Update the tool",action="store_true")
args = parser.parse_args()

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

def rate_limiting(url):
    print("Send multiple HTTP requests... Verify the rate limiting is exists...")
    for send in range(20):
        response = requests.get(url)
    if response.ok:
        print("RATE LIMITING [\033[1;32;40mVULNERABLE \033[0m]")
    else:
        print("RATE LIMITING [\033[0;31;47mNOT VULNERABLE\033[0m]")
        for by in range(15):
            bypass = requests.get(url, headers={"X-Forwarded-For": "127.0.0.1"})
        if bypass.ok:
            print("RATE LIMITING BYPASS [\033[1;32;40mVULNERABLE\033[0m] - with Header 'X-Forwarded-For'")
        else:
            print("RATE LIMITING BYPASS [\033[0;31;47mNOT VULNERABLE\033[0m]")
def verify(url):
    pedido = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
    req = pedido.headers
    ## Verificar se tem o header Server
    try:
        print("Server: ", req['Server'])
    except KeyError:
        print("Server header [NOT EXIST]")

    ## Verificar se tem o header X-XSS-Protecion
    try:
        if req['X-XSS-Protection'] == "0":
            print("XSS protection [\033[1;32;40mVULNERABLE\033[0m]")
        elif req['X-XSS-Protection'] == "1":
            print("XSS protection [\033[0;31;47mNOT VULNERABLE\033[0m]")
        elif req['X-XSS-Protection'] == "1; mode=block":
            print("XSS protection [\033[0;31;47mNOT VULNERABLE \033[0m]")
        else:
            print("XSS protection [\033[0;31;47mNOT VULNERABLE \033[0m] - ", req['X-XSS-Protection'])
    except KeyError:
        print("XSS protection [\033[1;32;40mVULNERABLE \033[0m] (not exist header!)")
    ## Verificar se é vulneravel a Clickjacking
    try:
        if req['X-Frame-Options'] == "SAMEORIGIN":
            print("Clickjacking [\033[0;31;47mNOT VULNERABLE \033[0m]")
        else:
            print("Clickjacking [\033[0;31;47mNOT VULNERABLE\033[0m]")
    except KeyError:
        print("Clickjacking [\033[1;32;40mVULNERABLE \033[0m]")

try:
    if args.url:
        print("URL: ", args.url)
        verify(args.url)
        rate_limiting(args.url)
    if args.version:
        print("\n")
        print("Developed by "+ __author__)
        print("Version of tool: "+ __version__)
    if args.update:
        ## Verify updates in repository github
        reqs = requests.get("https://raw.githubusercontent.com/hohky/Webber/main/options.json")
        options = reqs.json()
        if options['version'] == __version__:
            print("The tool is up to date!")
        else:
            print("New Version: {} \n Update in https://github.com/hohky/Webber" .format(reqs.text))
except ConnectionError:
    print("\r ({}) Connection error!" .format(time.strftime("%X")))
    
except KeyboardInterrupt:
    print("\r ({}) Action canceled by user!" .format(time.strftime("%X")))

except MissingSchema:
    print("\r ({}) Invalid URL!" .format(time.strftime("%X")))

## Verify version of Python
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

if __name__ != '__main__':
    sys.exit()
