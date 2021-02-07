# Made by HooS
import requests
import argparse
import time
import sys
from requests.exceptions import ConnectionError
from requests.exceptions import MissingSchema

__version__ = 1.0
__author__ = 'HooS'

parser = argparse.ArgumentParser(description="Para ver a geolocalização de um endereço de IP sem abrir uma única página")
parser.add_argument("-u", "--url", help="Indicar o URL")
parser.add_argument("-v", "--version", help="Indicate the version of this tool'", action="store_true")
parser.add_argument("--update", help="Update the tool",action="store_true")
args = parser.parse_args()

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

def rate_limiting(url):
    print("Send multiple HTTP requests... Verify the rate limiting is exists...")
    response = requests.get(url)
    for send in range(50):
        response = requests.get(url)
        print(response.status_code)
    if response.ok:
        print("RATE LIMITING [VULNERABLE]")
    else:
        print("RATE LIMITING [NOT VULNERABLE]")
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
            print("XSS protection [VULNERABLE]")
        elif req['X-XSS-Protection'] == "1":
            print("XSS protection [NOT VULNERABLE]")
        elif req['X-XSS-Protection'] == "1; mode=block":
            print("XSS protection [NOT VULNERABLE]")
        else:
            print("XSS protection [NOT VULNERABLE] - ", req['X-XSS-Protection'])
    except KeyError:
        print("XSS protection [VULNERABLE] (not exist header!)")
    ## Verificar se é vulneravel a Clickjacking
    try:
        if req['X-Frame-Options'] == "SAMEORIGIN":
            print("Clickjacking [NOT VULNERABLE]")
        else:
            print("Clickjacking [NOT VULNERABLE]")
    except KeyError:
        print("Clickjacking [VULNERABLE]")

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