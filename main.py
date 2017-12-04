#!/usr/bin/env python
#-*- coding: utf-8 -*
import urllib
import json
import os
import pickle
import connect_apiai
import Getprice
import PredP
import util
import Terms
import numpy as np

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
    print(dataSend)
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
        answer = connect_apiai.get_apiai(ai,content)
        print(answer)
        return jsonify({"message":{"text":answer}})
        

    elif u"처음으로" in content:
        dataSend ={ 
           "message": {
                "text": "처음으로 돌아갑니다."
            },
            "keyboard":{
                "type" : "buttons",
                "buttons" : ['현재 주가 확인','내일 예측 주가 확인','투자자 성향분석', '도움말']
            }
        }
        print(type(dataSend))
        print(type(dataSend)==dict)
        return jsonify(dataSend)
    else:
        answer = connect_apiai.get_apiai(ai,content)
        print(type(answer))
        print(answer)
        if type(answer) == dict:
            return jsonify(answer)
        else:    
            print(type(answer))
            print(answer)
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
    print(res)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    
    return r

def makeWebhookresult(req):
    if req.get("result").get("action") == "RTP" :

        result = req.get("result")
        parameters = result.get("parameters")
        if  parameters.get('stocks')!="":
            product = str(parameters.get("stocks"))
            print(product)
            code = Getprice.get_stockcode(product)
            RTP = Getprice.get_realtime(code)

       
        speech = str(product)+"의 현재 가격은 "+str(RTP)+"원 입니다."

        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "quantec"
        }
    elif req.get("result").get("action") == "future" :

        result = req.get("result")
        parameters = result.get("parameters")
        print(parameters.get('stcoks')!="")
        if  parameters.get('stocks')!="":
            product = str(parameters.get("stocks"))
            print(product)
            FP = PredP.get_future(product)
        if FP != " ":
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
            print(terms)
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
        
    elif req.get("result").get("action") == "Time":
        time = util.get_time()
        speech = "현재 시간은 "+ time
        
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
        print(contexts)
        parameters = contexts.get("parameters")
        print(parameters)
        score = 0
        for i in range(1,11):
            col = parameters.get("Step"+str(i))
            col = int(col)-1
            score += get_pattern.get_score(i,col)
        score = score/47*100
        
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
