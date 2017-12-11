#!/usr/bin/env python
#-*- coding: utf-8 -*
import urllib
import json
import os
import pickle
import connect_apiai
import Getprice
import PredP
import Terms
import numpy as np
import pandas as pd

import get_pattern
from flask import jsonify
from flask import Flask
from flask import request
from flask import make_response


import os.path
import sys
import json
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
CLIENT_ACCESS_TOKEN = 'f6e72afa001444d18c4fceeb9061b7f7'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
KEY =  get_pattern.KeyBoard
count = 0


# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> This is Quantec </h1>"

@app.route('/keyboard')
def Keyboard():
    
    dataSend = {
        "type" : "buttons",
        "buttons" : KEY.buttons
    }
    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    print(dataReceive)
    if content == u"현재 주가 확인":
        answer = connect_apiai.get_apiai(ai,content)
        return jsonify({"message":{"text":answer}})

    elif content == u"내일 예측 주가 확인":
        dataSend ={ 
           "message": {
                "text": "주가 예측 기능입니다.\n예측값들은 모두 딥러닝을 이용해 도출한 값이며 실제 투자에 있어 참고 용도로만 사용하시기 바랍니다.\n아래 버튼에서 원하시는 기능을 선택하세요"
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.fp1
            }
        }
        return jsonify(dataSend)
    
    elif u"금융 상품 추천" in content:
        dataSend ={ 
           "message": {
                "text": "고객님의 투자 성향을 선택해 주세요."
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.tendency
            }
        }
        return jsonify(dataSend)
    
    elif u"예측 서비스 종목 리스트" in content:
        a = pd.read_csv("pred.csv",dtype='str',encoding='utf-8',header=None,index_col=False)
        tmp = a[0]
        string = ""
        print(tmp)
        print(len(tmp))
        for i in range(1,len(tmp)):
            string += tmp[i]+" /"
        dataSend ={ 
           "message": {
                "text": "서비스가 제공되는 종목들은 다음과 같습니다.\n"+string
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.fp2
            }
        }
        return jsonify(dataSend)
    
    elif u"처음으로" in content:
        dataSend ={ 
           "message": {
                "text": "처음으로 돌아갑니다."
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.buttons
            }
        }
        return jsonify(dataSend)
    
    elif u"금융 용어 사전" in content:
        dataSend ={ 
           "message": {
                "text": "금융 용어 사전 기능입니다.\n 제공되는 기술은 다음과 같습니다."
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.terms1
            }
        }
        return jsonify(dataSend)
    
    elif u"금융용어 사전 리스트" in content:
        a = pd.read_excel("terms.xlsx",header=None)
        tmp = a[0]
        str = ""
        for i in range(1,len(tmp)):
            str += tmp[i]+" /"
        dataSend ={ 
           "message": {
                "text": "설명 가능한 용어는 다음과 같습니다.\n"+str
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.terms2
            }
        }
        return jsonify(dataSend)
    
    elif u"도움말" in content:
        msg = "모두의 금융 알리미 quantec 입니다. 현재 제공되는 기능은 다음과 같습니다.\n[현재주가확인, 투자자 성향분석, 금융 상품 추천, 내일 예측 주가 확인, 금융 용어 사전]\n현재 주가 확인 서비스는 국내 증권에만 한정하여 제공되고 있습니다.\n"
        msg += "금융 상품 추천 서비스는 금융투자협회에서 실제 운용되고 있는 금융 상품들을 6개월 수익률을 기준 수익 상위 5개 상품을 제공합니다."
        dataSend ={ 
           "message": {
                "text": msg
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : KEY.buttons
            }
        }
        return jsonify(dataSend)
        
    else:
        answer = connect_apiai.get_apiai(ai,content)
        if type(answer) == dict:
            print("@")
            return jsonify(answer)
        
        return jsonify({"message":{"text":answer}})

 

"""
@app.route('/message', methods=['POST'])    
def message():
    
    dataReceive = request.get_json()
    content = dataReceive['content']
    answer = connect_apiai.get_apiai(ai,content)
    print(answer)
    return jsonify({"message":{"text":answer}})
"""

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeWebhookresult(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookresult(req):
    if req.get("result").get("action") == "RTP" :

        result = req.get("result")
        parameters = result.get("parameters")
        if parameters.get('stocks')=="":
            return "확인하고 싶은 주식 종목을 입력해 주세요"
        elif  parameters.get('stocks')!="":
            product = str(parameters.get("stocks"))
            code = Getprice.get_stockcode(product)
            RTP = Getprice.get_realtime(code)

       
        speech = str(product)+"의 현재 가격은 "+str(RTP)+"원 입니다."

        print("Response:")
        print(speech)
    
        return speech
        
    elif req.get("result").get("action") == "futures" :

        result = req.get("result")
        parameters = result.get("parameters")
        if parameters.get('stocks')=="":
            return "확인하고 싶은 주식 종목을 입력해 주세요"
        elif  parameters.get('stocks')!="":
            product = str(parameters.get("stocks"))
            FP = PredP.get_future(product)
        if FP != "":
            speech = str(product)+"의 다음 거래일 가격은 "+str(FP)+"원 입니다."
        else:
            speech = "해당 종목의 가격 예상 시스템은 추후에 구현됩니다."
        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "quantec"
        }
    
    elif req.get("result").get("action") == "terms" :   
        
        result = req.get("result")
        parameters = result.get("parameters")

        if  parameters.get('terms')!="":
            terms = str(parameters.get("terms"))
            explain = Terms.get_explain(terms)

       
        speech = str(terms)+"의 뜻은 다음과 같습니다. "+explain+"\n"

        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "quantec"
        }
        
    elif req.get("result").get("action") == "survey":
        result = req.get("result")
        parameters = result.get("parameters")
        print(parameters)
        
        
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "quantec"
        }
    elif req.get("result").get("action") == "score":
        result = req.get("result")
        contexts = result.get("contexts")[0]
        parameters = contexts.get("parameters")
        score = 0
        frame = [[0,0,0,0,0],
         [4,4,3,2,1],
         [1,2,3,4,5],
         [-1,2,3,5,5],
         [1,2,3,4],
         [5,4,3,2,1],
         [3,2,1],
         [5,4,3,2,1],
         [-2,2,4,6],
         [2,3,4,5],
         [5,4,-2,-2],
        ]
        for i in range(1,11):
            col = parameters.get("Step"+str(i))
            col = int(col)-1
            tmp = frame[i][col]
            score += tmp
        score = int(score/47*100)

        if score>= 70:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 공격투자형 입니다."
            print(speech)
            return {
                "speech": speech,
                "displayText": speech,
                #"data": {},
                # "contextOut": [],
                "source": "quantec"
            }
        elif score>=60:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 적극투자형 입니다."
            print(speech)
            return {
                "speech": speech,
                "displayText": speech,
                #"data": {},
                # "contextOut": [],
                "source": "quantec"
            }
        elif score>=50:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 위험중립형 입니다."
            print(speech)
            return {
                "speech": speech,
                "displayText": speech,
                #"data": {},
                # "contextOut": [],
                "source": "quantec"
            }
        elif score>= 40:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 안정추구형 입니다."
            print(speech)
            return {
                "speech": speech,
                "displayText": speech,
                #"data": {},
                # "contextOut": [],
                "source": "quantec"
            }
        else:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 안정형 입니다."
            return {
                "speech": speech,
                "displayText": speech,
                #"data": {},
                # "contextOut": [],
                "source": "quantec"
            }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
