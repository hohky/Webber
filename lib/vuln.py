import requests
from .common.colors import *

class common:
    
    def rate_limiting(url):
        print("Send multiple HTTP requests... Verify the rate limiting is exists...",end="\r")
        for send in range(20):
            response = requests.get(url)
        if response.ok:
            print(f"[{Green}+{White}] RATE LIMITING [{Green}VULNERABLE{White}]", end="\r")
        else:
            print(f"[{Red}-{White}] RATE LIMITING [{Red}NOT VULNERABLE{White}]")
            for by in range(15):
                bypass = requests.get(url, headers={"X-Forwarded-For": "127.0.0.1"})
            if bypass.ok:
                print(f"[{Green}+{White}] RATE LIMITING BYPASS [{Green}VULNERABLE{White}] - with Header 'X-Forwarded-For'")
            else:
                print(f"[{Red}-{White}] RATE LIMITING BYPASS [{Red}NOT VULNERABLE{White}]")

        
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
