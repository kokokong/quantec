#-*- coding: utf-8 -*
import os.path
import sys
import json
import get_pattern
import Getprice
import PredP
import Terms
import recom

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
    parameter = response_obj.get('result').get('parameters')
    action = response_obj.get("result").get("action")

    if action == "SURVEY":
        for i in range(1,11):
            if parameter.get("Step"+str(i)) =="":
                print(i)
                dataSend = get_pattern.update_keyboard(i)
                return dataSend
    elif action == "score":
        result = response_obj.get("result")
        contexts = result.get("contexts")[0]
        parameters = contexts.get("parameters")
        score = 0
        frame = [[0,0,0,0,0,0],
         [0,4,4,3,2,1],
         [0,1,2,3,4,5],
         [0,-1,2,3,5,5],
         [0,1,2,3,4],
         [0,5,4,3,2,1],
         [0,3,2,1],
         [0,5,4,3,2,1],
         [0,-2,2,4,6],
         [0,2,3,4,5],
         [0,5,4,-2,-2],
        ]
        print(parameters)
        for i in range(1,11):
            col = parameters.get("Step"+str(i))
            print(col)
            if col !=None:
                col = int(col)
                tmp = frame[i][col]
                score += tmp
        score = int(score/47*100)

        if score>= 70:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 공격투자형 입니다."
        elif score>=60:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 적극투자형 입니다."
        elif score>=50:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 위험중립형 입니다."
        elif score>= 40:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 안정추구형 입니다."
        else:
            speech = "고객님의 투자 성향 점수는 "+str(score)+"점으로 안정형 입니다."
        
        dataSend = {
                "message": {
                    "text": speech
                },
                "keyboard": {
                    "type" : "buttons",
                    "buttons" : get_pattern.KeyBoard.survey
                }
        }
        return dataSend
        
    elif action == "RTP" :
        result = response_obj.get("result")
        parameters = result.get("parameters")
        if parameters.get('stocks')=="":
            return "확인하고 싶은 주식 종목을 입력해 주세요"
        elif  parameters.get('stocks')!="":
            product = str(parameters.get("stocks"))
            print(product)
            code = Getprice.get_stockcode(product)
            RTP = Getprice.get_realtime(code)
        speech = str(product)+"의 현재 가격은 "+str(RTP)+"원 입니다."
        
        dataSend = {
                "message": {
                    "text": speech
                },
                "keyboard": {
                    "type" : "buttons",
                    "buttons" : get_pattern.KeyBoard.rtp
                }
        }
        return dataSend
    elif action == "futures":
        result = response_obj.get("result")
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
        
        dataSend = {
                "message": {
                    "text": speech
                },
                "keyboard": {
                    "type" : "buttons",
                    "buttons" : get_pattern.KeyBoard.fp
                }
        }
        return dataSend
        
    elif action == "terms":
        result = response_obj.get("result")
        parameters = result.get("parameters")
        print(response_obj)
        if parameters.get("terms") =="":
            return "알고 싶은 금융 용어를 검색해 보세요"
        elif  parameters.get('terms')!="":
            terms = str(parameters.get("terms"))
            explain = Terms.get_explain(terms)
        speech = str(terms)+"의 뜻은 다음과 같습니다. "+explain
        
        dataSend = {
            "message": {
                "text": speech
            },
            "keyboard": {
                "type" : "buttons",
                "buttons" : get_pattern.KeyBoard.terms
            }
        }
        return dataSend
        
    elif action == "recom":
        result = response_obj.get("result")
        parameters = result.get("parameters")
        #"공격투자형","적극투자형","위험중립형","안정추구형","안정형"
        if parameters.get("tendency") =="":
            dataSend = {
                "message": {
                    "text": "고객님의 투자 성향을 선택해 주세요"
                },
                "keyboard": {
                    "type" : "buttons",
                    "buttons" : get_pattern.KeyBoard.tendency
                }
            }
            return dataSend
        elif parameters.get("tendency") !="":
            if parameters.get("tendency") == "exhigh":
                speech = recom.Recom(parameters.get("tendency"))    
            elif parameters.get("tendency") =="high":
                speech = recom.Recom(parameters.get("tendency"))    
            elif parameters.get("tendency") =="normal":
                speech = recom.Recom(parameters.get("tendency"))    
            elif parameters.get("tendency") =="low":
                speech = recom.Recom(parameters.get("tendency"))    
            elif parameters.get("tendency") =="exlow":
                speech = recom.Recom(parameters.get("tendency"))
            
            dataSend = {
                "message": {
                    "text": speech
                },
                "keyboard": {
                    "type" : "buttons",
                    "buttons" : get_pattern.KeyBoard.end
                }
            }
            return dataSend
    answer = response_obj["result"]["fulfillment"]["speech"]
    return answer
