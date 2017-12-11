import pandas as pd
import numpy as np

def Recom(parameter):
    print(parameter)
    port = pd.read_excel(parameter+".xlsx",header=None)
    print(port)
    s = ""
    for i in range(5):
        tmp = port.iloc[i]
        s += (tmp[0]+"\n: ")
        st = np.array2string(tmp[1])
        s += (st+"\n")
    return s