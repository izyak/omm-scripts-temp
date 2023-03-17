import json
import requests
from helpers.mysql import connection
from helpers.logger import logger
from checkscore.repeater import retry
from helpers.constants import ADDRESS, MAINNET_ENDPOINT


SQL_INSERT_BOMM_STATS = (
    "INSERT INTO bomm_stats"
    "(user, amount, expire)"
    "VALUES (%s, %s, %s)"
)

SQL_INSERT_BOMM_USERS = ("INSERT IGNORE bomm_users (user) VALUES (%s) ON DUPLICATE KEY UPDATE user=user;")

SQL_DROP_BOMM_STATS = ("TRUNCATE TABLE bomm_stats")

class BOMMAnalyticsData(object):
    def __init__(self):
        self.userList = []
        self.lockDetails = []

    def make_rpc_dict(self, method: str, params) -> str:
        rpc_dict = {
            'jsonrpc': '2.0',
            'method': 'icx_call',
            'id': 1234,
            'params': {
                "from": "hx0000000000000000000000000000000000000000",
                "to": ADDRESS["BOOSTED_OMM"],
                "dataType": "call",
                "data": {
                    "method": f"{method}",
                    "params": params
                }
            }
        }
        return json.dumps(rpc_dict)

    @retry(Exception, tries=5, delay=1)
    def get_request(self, payload: str):
        r = requests.post(MAINNET_ENDPOINT, data=payload)
        return json.loads(r.text)['result']

    def fetch_user_list(self, skip: int):
        params = {
            "start": f'{skip}',
            "end": f'{skip+100}',
        }
        payload = self.make_rpc_dict("getUsers", params)
        data = self.get_request(payload)
        self.userList.extend(data)
        if len(data) == 100:
            self.fetch_user_list(skip+100)

    def fetch_lock_details(self, user: str):
        params = {'_owner': user}
        payload = self.make_rpc_dict("getLocked", params)
        response = self.get_request(payload)
        self.lockDetails.append([user, int(response.get("amount"), 16)/10**18, int(response.get("end"), 16)//1000_000])

    def all_user_details(self):
        for user in self.userList:
            self.fetch_lock_details(user)

    def save_analytics(self):
        self.all_user_details()
        logger.info(f"... updating bOMM info ...")
        for detail in self.lockDetails:
            _val = (detail[0], detail[1], detail[2])
            logger.info("%s,%s,%s" % _val)
            with connection.cursor() as cursor:
                cursor.execute(SQL_INSERT_BOMM_STATS, _val)
                cursor.execute(SQL_INSERT_BOMM_USERS, (detail[0]))



if __name__ == "__main__":
    bomm = BOMMAnalyticsData()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_DROP_BOMM_STATS)
        bomm = BOMMAnalyticsData()
        bomm.fetch_user_list(0)
        bomm.save_analytics()
        connection.commit()
