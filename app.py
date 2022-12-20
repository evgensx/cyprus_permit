import requests
from bs4 import BeautifulSoup
import html
import time


# Введите свой логин и пароль  v                       v
credentials = {'sUsername': 'login', 'sPassword': 'password'}

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
session = requests.Session()

def get_token() -> str:
    _url = 'https://studentgateway.gov.ct.tr/main.asmx/_StayPermitLogin'
    _headers = {'Host': 'studentgateway.gov.ct.tr',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
                'Accept': 'application/json, text/plain, */*'}
    _data= credentials
    _response = session.post(_url, data=_data, headers=_headers)
    session.close()
    soup = BeautifulSoup(_response.text, "xml")
    _tocken = soup.string.lstrip('001: ').rstrip('|False')
    return _tocken


def auth(tocken=get_token()) -> str:
    _tocken = tocken
    _url = "https://studentgateway.gov.ct.tr/main.asmx/_GetStayApplicationInformation"
    _params = {'sHashedRecNo': _tocken}
    _headers = {'Host': 'studentgateway.gov.ct.tr',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://permissions.gov.ct.tr'
                }
    _response = session.get(_url, params=_params, headers=_headers)
    session.close()
    _soup = BeautifulSoup(html.unescape(_response.text), "xml")
    _stage = _soup.ProcessID.string

    progress = {'IK001': 'Initialisation', 'IK002': '1/7 Application', 'IK100': '2/7 Document Upload',
                'IK150': '3/7 Police', 'IK070': '4/7 State Hospital', 'IK300': '60% 5/7 Immigration Office'}
    match _stage:
        case 'IK001':
            return f'Progress: {progress["IK001"]}'
        case 'IK002':
            return f'Progress: {progress["IK002"]}'
        case 'IK100':
            return f'Progress: {progress["IK100"]}'
        case 'IK150':
            return f'Progress: {progress["IK150"]}'
        case 'IK070':
            return f'Progress: {progress["IK070"]}'
        case 'IK300':
            return f'Progress: {progress["IK300"]}'
        case _:
            return f'New stage! {_stage}'


def main():
    print(auth())
    print('Press [Ctrl]+[C] for exit')

try:
    main()
    time.sleep(5)
except KeyboardInterrupt:
    exit()