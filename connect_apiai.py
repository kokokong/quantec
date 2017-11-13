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

def get_apiai(ai, message):
    request = ai.text_request()
    request.lang = 'ko'
    request.query = message

    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    answer = response_obj["result"]["fulfillment"]["speech"]
    
    return answer
