import requests
import json
import concurrent.futures
import os
from checkscore.repeater import retry

GEOMETRY_LOG_API = "https://tracker.icon.community/api/v1/transactions"
LENDING_POOL = "cxcb455f26a2c01c686fa7f30e1e3661642dd53c0d"
# this value might not be enough, so check the skip for limit 100 till which data exists
UPTO = 80000

@retry(Exception, tries=3, delay=1, back_off=2)
def get_log_request(skip, method, score):
    payload = {'skip': skip, 'method': method, "limit": 100, "to": score}
    req = requests.get(GEOMETRY_LOG_API, params=payload)
    return json.loads(req.text)

stakers_list = []
skip = 0
threshold_reached = False

def get_staked_balance(addr: str):
    rpc_dict = {
            'jsonrpc': '2.0',
            'method': 'icx_call',
            'id': 1234,
            'params': {
                "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "to": "cx1a29259a59f463a67bb2ef84398b30ca56b5830a",  
                "dataType": "call",
                "data": {
                    "method": "staked_balanceOf",
                    "params": {
                        "_owner": addr 
                    }
                }
           }
    }
    r = requests.post("https://ctz.solidwallet.io/api/v3", data=json.dumps(rpc_dict))
    return int(json.loads(r.text)['result'], 0)

def get_stakers(skip):
    try:
        data = get_log_request(skip, "stake", LENDING_POOL)
        for i in data:
            addr = i.get('from_address')
            if addr not in stakers_list:
                staked_balance = get_staked_balance(addr)
                if staked_balance > 0:
                    stakers_list.append(addr)
    except:
        pass

with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    executor.map(get_stakers, [i for i in range(0, UTPO, 100)])

with open ('omm-stakers.json','w') as outfile:
    json.dump(stakers_list, outfile)
