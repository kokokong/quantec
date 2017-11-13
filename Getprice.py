import pandas as pd
import pandas_datareader.data as web
import datetime
import json
import requests


def get_realtime(code):
    print(code)
    code = code.zfill(6)
    rsp = requests.get('https://finance.google.com/finance?q='+code+'&output=json')
    print(rsp)
    if rsp.status_code in (200,):
        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
        rt_price = fin_data['l']

    return rt_price
    
