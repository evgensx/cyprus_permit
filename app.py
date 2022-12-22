import requests
from bs4 import BeautifulSoup
import html
import time
from dotenv import dotenv_values

env = dotenv_values('.env')

# Введите свой логин и пароль в файле '.env'
credentials = {'sUsername': env.get('LOGIN'), 'sPassword': env.get('PASSWORD')}

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

    _progress = {'IK001': 'Initialisation', 'IK002': '1/7 Application', 'IK100': '2/7 Document Upload',
                 'IK150': '3/7 Police', 'IK070': '4/7 State Hospital', 'IK300': '60% 5/7 Immigration Office'}
    if _stage in _progress.keys():
        return(_progress.get(_stage))
    else:
        return(f'New stage is {_stage}!')

def main():
    print('Progress:', auth())
    print('Press [Ctrl]+[C] for exit')
    time.sleep(5)

try:
    main()
except KeyboardInterrupt:
    exit()
except AttributeError:
    print('Set login and password')
