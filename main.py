#!/usr/bin/env python
#-*- coding: utf-8 -*

import urllib
import json
import os
import Getprice
import pickle
import connect_apiai


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
CLIENT_ACCESS_TOKEN = '1885ee7d899e40b6b3ab98bee443a2cb'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> 카페 뿌리입니다! ! </h1>"

@app.route('/keyboard')
def Keyboard():
    datasend = {
        "type":"text"
    }

    return jsonify(datasend)
    

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
        print(parameters)
        print(parameters.get('stcoks')!="")
        if  parameters.get('stocks')!="":
            product = str(parameters.get("stocks"))
            RTP = Getprice.get_realtime(product)

       
        speech = str(product)+"의 현재 가격은 "+str(RTP)+"원 입니다."

        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-onlinestore-shipping"
        }
    elif req.get("result").get("action") == "order.noncoffee":
        result = req.get("result")
        parameters = result.get("parameters")
        print(parameters)
        
        if parameters.get('non_coffee')!="":
            product = parameters.get("non_coffee")
            cost = getcost.get_cost("non_coffee",product)
        if parameters.get("Hot") =='ICE':
            cost += 500
        if parameters.get("takeout") == 'Takeout':
            cost -= 500
            
        speech = "주문하신 "+str(product)+" 의 가격은 "+str(cost)+"원 입니다."
            
        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "cafe-bburi"
        }
    elif req.get("result").get("action") == "order.bakery":
        result = req.get("result")
        parameters = result.get("parameters")
        print(parameters)
        
        if parameters.get('bakery')!="":
            product = parameters.get("bakery")
            cost = getcost.get_cost("bakery",product)
        speech = "주문하신 "+str(product)+" 의 가격은 "+str(cost)+"원 입니다."
            
        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "cafe-bburi"
        }  
        
        
    elif req.get("result").get("action") == "callMenu":
        result = req.get("result")
        parameters = result.get("parameters")
        category = parameters.get("Menu")
        Menu = getcost.get_menu(category)
   
        speech = str(category)+" 메뉴는 "+"/ ".join(Menu)+" 가 있습니다.\n"
        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "cafe-bburi"
        }
        
    elif req.get("result").get("action") == "getprice":
        result = req.get("result")
        parameters = result.get("parameters")
        category = parameters.get("product")
        price = getcost.get_price(category)
   
        speech = str(category)+"의 가격은 "+str(price)+"원 입니다."
        print("Response:")
        print(speech)
    
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "cafe-bburi"
        }
    else:
        return {}
        
def makeWebhookmenu(req):
    if req.get("result").get("action") != "call.menu" :
        return {}
        
    result = req.get("result")
    parameters = result.get("parameters")
    category = parameters.get("Menu")
    Menu = getcost.get_menu(category)
   
    speech = str(category)+" 메뉴는 "+" /".join(str(Menu))+" 가 있습니다.\n"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "cafe-bburi"
    }
        
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
