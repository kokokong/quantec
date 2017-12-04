#-*- coding: utf-8 -*
import datetime

def get_time():
    now = datetime.datetime.now()
    hour   = now.hour
    minute = now.minute
    
    return str(hour)+"시 "+str(minute)+"분 입니다."
    