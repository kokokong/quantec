import pandas as pd

def get_explain(terms):
    tmp = pd.read_excel("terms.xlsx",dtype=str)
    idx = 0
    for i in range(len(tmp)):
        if(terms == tmp['용어'][i]):
            idx = i
            break
    explain = tmp['설명'][idx]
    return explain
