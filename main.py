import json
import os
import sys
import time
import requests
import yaml
from RSA import GetContent

def log(info):
    log_file = "connect.txt"
    print(info.strip())
    with open(log_file, "a") as f:
        f.write(info.strip() + "\n")


def login(Id, password, exponent, modulus):
    url = 'http://10.10.9.9:8080/eportal/InterFace.do?method=login'
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    content = GetContent(Id, password, exponent, modulus)
    try:
        response = requests.post(url, content, headers=header, timeout=10)
        content = json.loads(response.text)
        encoding = response.encoding
        if content['result'] == 'fail':
            msg = content['message'].encode(encoding).decode('utf-8')
            log(msg)
        else:
            log("login at --> " + time.asctime(time.localtime(time.time())))
        return
    except Exception as info:
        log("login wrong:" + str(info))


def ping(host, n):
    cmd = "ping {} {} {} > ping.log".format(
        "-n" if sys.platform.lower() == "win32" else "-c",
        n,
        host,
    )
    return 0 == os.system(cmd)


def pong():
    return ping("www.baidu.com", 2) or ping('8.8.8.8', 2)


if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        user = yaml.load(f, Loader=yaml.FullLoader)['User']
    while True:
        if pong():
            time.sleep(user['wait_ping'])
        else:
            login(user['Id'], user['password'], user['exponent'], user['modulus'])
            time.sleep(user['wait_connect'])
