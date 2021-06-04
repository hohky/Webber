#!/usr/bin/python3

import requests
import argparse
import time
import sys
from requests.exceptions import ConnectionError, MissingSchema, InvalidSchema, TooManyRedirects

## Webber functions
from lib.files import Fuzz
from lib.params import Vulns
from lib.waf import waf
from lib.exceptions import *
from lib.common.colors import *
from lib.vuln import common



"""
Copyright (c) 2020-2021 HooS developer (https://github.com/hohky/Webber)
"""

__version__ = 1.3
__author__ = 'HooS'

parser = argparse.ArgumentParser(description="Scan website for searching vulnerability!")
parser.add_argument("-u", "--url", help="Indicar o URL")
parser.add_argument("-v", "--version", help="Indicate the version of this tool", action="store_true")
parser.add_argument("-sr", "--skip-rate", help="Skip the Rate limiting", action="store_true")
parser.add_argument("-sf", "--skip-fuzzer", help="Skip the Fuzzer", action="store_true")
parser.add_argument("-sp", "--skip-params", help="Skip the Params scanner", action="store_true")
parser.add_argument("--update", help="Update the tool",action="store_true")
args = parser.parse_args()


if sys.version_info[0] < 3:
    raise VersionOutdated("Must be using Python 3")

def banner():
    print(f'''{Cyan} __      __   _    _             
 \ \    / /__| |__| |__  ___ _ _ 
  \ \/\/ / -_) '_ \ '_ \/ -_) '_|
   \_/\_/\___|_.__/_.__/\___|_|  
                                 {White}''')



try:
    if args.url:
        fz = Fuzz(args.url) ## My class from lib.params
        vulner = Vulns(args.url) ## My class from lib.params
        banner()
        print("URL: ",Whiter, args.url, White)
        common.verify(args.url)
        waf(args.url)
        if not args.skip_rate:
           common.rate_limiting(args.url)
        if not args.skip_fuzzer:
            fz.check()
        if not args.skip_params:
            vulner.check_params()
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
            print(f"New Version: {options['version']} \nUpdate in https://github.com/hohky/Webber")
    else:
        banner()
        print("\nHelp command -> --help")
except ConnectionError:
    banner()
    print("\r({}{}{}) Connection Error!" .format(Redf,time.strftime("%X"), White))
    
except KeyboardInterrupt:
    banner()
    print("\r({}{}{}) Action canceled by user!" .format(Redf,time.strftime("%X"), White))

except MissingSchema:
    print("\r({}{}{}) Invalid URL!" .format(Redf,time.strftime("%X"), White))

except InvalidSchema:
    print("\r({}{}{}) Invalid URL!" .format(Redf,time.strftime("%X"), White))

except TooManyRedirects:
    print("\r({}{}{}) Too many Redirects!" .format(Redf,time.strftime("%X"), White))

except VersionOutdated:
    print("\r({}{}{}) Must be use Python 3!" .format(Redf,time.strftime("%X"), White))


if __name__ != '__main__':
    sys.exit()
