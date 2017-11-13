import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy
import json
import requests

def get_stockcode(product):
    tmp = pd.read_csv("stock_code.csv",dtype=str,encoding='utf-8')
    idx = 0
    for i in range(len(tmp)):
        if(product == tmp['회사명'][i]):
            idx = i
            break
    code = tmp['종목코드'][i]
    code = 'KRX:'+str(code)
    return code

def get_realtime(code):
    print(code)
    code = code.zfill(6)
    rsp = requests.get('https://finance.google.com/finance?q='+code+'&output=json')
    if rsp.status_code in (200,):
        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
        rt_price = fin_data['l']

    return rt_price
    
