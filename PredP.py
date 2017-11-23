#-*- coding: utf-8 -*-
import pandas as pd

def get_future(product):
    tmp = pd.read_csv("pred.csv",dtype=str,encoding='utf-8')
    idx = 0
    for i in range(len(tmp)):
        if(product == tmp['회사명'][i]):
            idx = i
            break
    price = tmp['예상가격'][idx]
    print(type(price))
    price = int(float(price))
    return price
    