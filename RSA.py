# coding：utf-8
import subprocess
import requests
import yaml
from urllib import parse


def RsaPasswordGet(file_name, userId, passwd, qeury, exponent, modulus):
    #pro = subprocess.run(f"node {file_name}", stdout=subprocess.PIPE)
    if(type(userId) == int):
        userId = str(userId)
    if (type(passwd) == int):
        passwd = str(passwd)
    passwd = passwd[::-1]       # 反转密码
    pro = subprocess.run(['node', file_name, userId, passwd, qeury, exponent, modulus], stdout=subprocess.PIPE)
    _token = pro.stdout
    rsa_passwd = _token.decode().strip()
    return rsa_passwd


def getQueryString():
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    try:
        response = requests.post('http://10.10.9.9:8080', headers=header,timeout=2)
        queryString = response.text
        queryString = queryString.split('?')[1]
        # queryString = queryString.replace('=', '%253D')
        # queryString = queryString.replace('&', '%2526')
        # queryString = queryString.replace(' ', '52')
        queryString = queryString[:-11]
        queryString = parse.quote(parse.quote(queryString))
        queryString = queryString.replace('/', '%252F')
        return queryString
    except:
        print("It is possible that you have not yet selected the campus network on your computer")

def GetContent(Id, password, exponent, modulus):
    query = getQueryString()
    rsa_passwd = RsaPasswordGet('web_source/secure.js', Id, password, query, exponent,
                                modulus)
    return rsa_passwd

