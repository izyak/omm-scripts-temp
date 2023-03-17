import requests
import json
from datetime import datetime
from checkscore.repeater import retry
from helpers.logger import logger
from helpers.constants import TOKENS, US_PER_HR, ADDRESS
from pprint import pprint 
from helpers.mysql import connection

RESERVES = {v:k for k,v in TOKENS.items()}

SQL_INSERT_UTILIZATION_RATES = (
    "INSERT INTO omm_utilization_rates"
    "(reserve, timestamp, total_borrows, total_liquidity, total_borrows_usd, total_liquidity_usd, utilization_rate)"
    "VALUES (%s,%s,%s,%s,%s,%s,%s)"
)

class ReserveData(object):
    def __init__(self):
        super(ReserveData, self).__init__()
    
    @retry(Exception, tries=20, delay=1, back_off=2)    
    def _get_all_reserve_data(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "icx_call",
            "id": 1641454421714,
            "params": {
                "from": "hxbe258ceb872e08851f1f59694dac2558708ece11",
                "to": ADDRESS['DATA_PROVIDER'], 
                "dataType": "call",
                "data": {
                    "method": "getAllReserveData",
                    "params": {}
                }
            }
        }
        r = requests.post("https://ctz.solidwallet.io/api/v3", data=json.dumps(payload))
        return json.loads(r.text).get('result')

    def save(self):
        all_reserve_data = self._get_all_reserve_data()       

        for name, reserve_data in all_reserve_data.items():
            decimals = int(reserve_data.get('decimals'), 16)

            total_borrows = int(reserve_data.get('totalBorrows'), 16) / 10 ** decimals
            total_borrows_usd = int(reserve_data.get('totalBorrowsUSD'), 16) / 10 ** 18
            total_liquidity = int(reserve_data.get('totalLiquidity'), 16) / 10 ** decimals
            total_liquidity_usd = int(reserve_data.get('totalLiquidityUSD'), 16) / 10 ** 18
            
            utilization_rate = total_borrows / total_liquidity * 100
            current_timestamp = int(datetime.timestamp(datetime.now()))

            _val = (name.upper(), current_timestamp, total_borrows, total_liquidity, total_borrows_usd, total_liquidity_usd, utilization_rate)
            logger.info(f"... inserting {name} info ...")
            logger.info("%s,%s,%s,%s,%s,%s,%s" % _val[:7])
            with connection.cursor() as cursor:
                cursor.execute(SQL_INSERT_UTILIZATION_RATES, _val)

if __name__ == "__main__":
    with connection:
        reserveData = ReserveData()
        reserveData.save()
        connection.commit()