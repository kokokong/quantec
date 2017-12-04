#-*- coding: utf-8 -*
from flask import jsonify
from flask import Flask
from flask import request
from flask import make_response
import numpy as np

        
class KeyBoard:
    buttons = ['현재 주가 확인','내일 예측 주가 확인','투자자 성향분석', '도움말']
    
    Q1 =  ['19세 이하','20세 이상 40세 이하','41세 이상 50세 이하','51세 이상 60세 이하', '61세 이상']
    
    Q2 =  ['6개월 미만','6개월 이상 1년 미만','1년 이상 2년 미만','3년 이상']
    
    Q3 = ['은행 예금, 은행 적금, 국채, MMF, CMA 등',
          '금융채, 신용도가 높은 회사채, 채권형 펀드, 원금보장형 ELS 등',
          '신용도 중간 등급의 회사채, 원금의 일부만 보장되는 ELS, 혼합형 펀드',
          '신용도가 낮은 회사채, 주식, 원금이 보장되지 않는 ELS, 시장수익률 수준의 수익을 추구하는 주식형펀드',
          'ELW, 선물옵션, 시장수익률 이상의 수익을 추구하는 주식형펀드, 파생상품에 투자하는 펀드, 주식 신용거래 등']
    Q4 = ['스스로 투자의사 결정을 내려 본 경험이 없다.',
          '주식과 채권의 차이를 구분할 수 있다.',
          '투자 할 수 있는 대부분의 금융상품의 차이를 구별할 수 있다.',
          '금융상품을 비롯하여 모든 투자대상 상품의 차이를 이해할 수 있는 정도']
    Q5 = ['10 퍼센트미만','10 퍼센트 이상 20 퍼센트 미만','20 퍼센트 이상 30 퍼센트 미만','30 퍼센트 이상 40 퍼센트 미만','40 퍼센트 이상']
    
    Q6 = ['현재 일정한 수입이 발생하고 있으며, 향후 현재 수준을 유지하거나 증가할 것으로 예상',
          '현재 일정한 수입이 발생하고 있으나, 향후 감소하거나 불안정할 것으로 예상',
          '현재 일정한 수입이 없으며, 연금등이 주 수입원임']
          
    Q7 = ['10 퍼센트 미만','10 퍼센트 이상 20 퍼센트 미만','20 퍼센트 이상 30 퍼센트 미만','30 퍼센트 이상 40 퍼센트 미만','40 퍼센트 이상']
    
    Q8 = ['무슨 일이 있어도 투자 원금은 보장되어야 한다',
          '10 퍼센트 미만까지는 손실을 감내할 수 있을 것 같다 ',
          '20 퍼센트 미만까지는 손실을 감내할 수 있을 것 같다. ',
          '기대수익이 높다면 위험이 높아도 상관하지 않겠다.']
    Q9 = ['5천만원이내','7천만원이내','1억원이내','1억원이상']
    
    Q10 = ['여유자금운용','퇴직금운용','생계자금 마련','대출금 상환','기타']


def update_keyboard(i):
    if i == 0:
        dataSend = {
                    "message": {
                        "text": "고객님의 연령은 어떻게 되십니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.buttons
                        }
                    }
    if i ==1:
        dataSend = {
                    "message": {
                        "text": "고객님의 연령은 어떻게 되십니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q1
                        }
                    }
    elif i ==2:
        dataSend = {
                    "message": {
                        "text": "고객님께서 투자하고자 하는 자금의 투자 가능 기간은 얼마나 되십니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q2
                    }
                }
    elif i ==3:
        dataSend = {
                    "message": {
                        "text": "다음 중 고객님의 투자 경험과 가장 가까운 것은 어느 것입니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q3
                    }
                }
    elif i ==4:
        dataSend = {
                    "message": {
                        "text": "고객님께서는 금융 투자에 대한 본인의 지식수준이 어느 정도라고 생각하십니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q4
                    }
                }
    elif i ==5:
        dataSend = {
                    "message": {
                        "text": "전체 금융자산(부동산 제외)중 투자하고자하는 자금의 비중은 어느 정도 차지합니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q5
                    }
                }
    elif i ==6:
        dataSend = {
                    "message": {
                        "text": "고객님의 수익원을 가장 잘 나타내는 것은 어느 것입니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q6
                    }
                }
    elif i ==7:
        dataSend = {
                    "message": {
                        "text": "총자산 대비 금융자산의 비중은 어느 정도 차지합니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q7
                    }
                }
    elif i ==8:
        dataSend = {
                    "message": {
                        "text": "고객님의 투자 원금에 손실이 발생할 경우 감수할 수 있는 손실 수준은 어느 것입니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q8
                    }
                    }
    elif i ==9:
        dataSend = {
                    "message": {
                        "text": "고객님의 연소득은 어느 정도 되십니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q9
                    }
                }
    elif i ==10:
        dataSend = {
                    "message": {
                        "text": "고객님의 투자목적은 무엇입니까?"
                    },
                    "keyboard": {
                        "type" : "buttons",
                        "buttons" : KeyBoard.Q10
                    }
                    }
    else:
        dataSend = {
                    "message": {
                        "text": "알수없군요"
                    },
                }
    return dataSend
    
    
def get_score(i,j):
    if(i<=10):
        frame = np.genfromtxt("score.csv",delimiter=',',dtype='int')
        score = frame[i][j]
        return score