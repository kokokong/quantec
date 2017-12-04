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
    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    name = response_obj['result']['metadata']['intentName'][:7]
    parameter = response_obj.get('result').get('parameters')
    print(name)
    print(len(name))
    if len(name) == 7:
        for i in range(1,11):
            if parameter.get("Step"+str(i)) =="":
                print(i)
                dataSend = get_pattern.update_keyboard(i)
                return dataSend

    answer = response_obj["result"]["fulfillment"]["speech"]
    return answer
