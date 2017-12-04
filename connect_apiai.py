#-*- coding: utf-8 -*
import os.path
import sys
import json
import get_pattern
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


def get_apiai(ai, message):
    request = ai.text_request()
    request.lang = 'ko'
    request.query = message
    print(message)
    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    print(response_obj)
    name = response_obj['result']['metadata']['intentName'][:7]
    parameter = response_obj.get('result').get('parameters')
    for i in range(1,11):
        if parameter.get("Step"+str(i)) =="":
            dataSend = get_pattern.update_keyboard(i)
            return dataSend
        """    
        print(parameter)
        print(type(parameter))
        a= parameter.keys()
        print(type(a))
        b = list(parameter)
        print(b)
        for i in range(1,11):
            a = "Step"+str(i)
            print(a)
            if parameter.get(a) == "":
                print(i)
                dataSend = get_pattern.update_keyboard(i)
                print(dataSend)
                return dataSend
        """
    answer = response_obj["result"]["fulfillment"]["speech"]
    print(answer)
    return answer
