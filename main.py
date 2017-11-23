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

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> This is Quantec </h1>"

@app.route('/keyboard')
def Keyboard():
    datasend = {
        "type":"text"
    }

    return jsonify(datasend)
    
@app.route('/message', methods=['POST'])    
def message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    answer = connect_apiai.get_apiai(ai,content)
    print(answer)
    return jsonify({"message":{"text":answer}})

@app.route('/webhook', methods=['POST'])
def webhook():
    
    req = request.get_json(silent=True, force=True)
    print("ip: ")
    print(request.headers.get('User-Agent'))
    print(req)
    print(request.remote_addr)
    res = makeWebhookresult(req)

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
        
        
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
