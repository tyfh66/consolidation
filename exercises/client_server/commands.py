import json
from datetime import datetime

def get_time():
    """ Basic command to return current system time in json"""
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")    
    return(json.dumps({'current_host_time': current_time}, indent=4))