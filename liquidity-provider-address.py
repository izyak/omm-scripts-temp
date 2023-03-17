import argparse
import csv
import json
import requests
import time
import sys

from checkscore.repeater import retry

LIMIT=1000
print(sys.getrecursionlimit())
sys.setrecursionlimit(LIMIT)
print(sys.getrecursionlimit())

API = 'https://tracker.icon.community/api/v1/logs'
OMM_sICX_POOL_ID = 0x7
LP_ADDED_TIMESTAMP = 1629954000000000
START = 600_000
THRESHOLD = START + LIMIT * 100
OMM_sICX = "cx687fa54d7b8328fc560dc7a68a0d44d7f1091a25"
print("THRESHOLD---",THRESHOLD)
# LP_ADDED_TIMESTAMP = 1640753927183022

ADDRESS = {
    'LENDING_POOL': 'cxcb455f26a2c01c686fa7f30e1e3661642dd53c0d',
    'oICX': 'cx0fb973aaab3a26cc99022ba455e5bdfed1d6f0d9',
    'reward': 'cx4f2d730ad969f5c839229de42184c5e47aefef6f',
    'DEX': 'cxa0af3165c08318e988cb30993b3048335b94af6c'
}


def argumentParser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-tkn", "--token", help="Token", type=str, default="oICX")
    parser.add_argument("-nid", "--nid", help="NID", type=int, default="1")

    args = parser.parse_args()

    return args


class LiquidityProvider(object):
    def __init__(self):
        super(LiquidityProvider, self).__init__()
        self.has_threshold_reach = False;
        self.wallets = []

    @retry(Exception, tries=20, delay=1, back_off=2)
    def _get_request(self, skip):
        print("skip---",skip)
        payload = {'skip': skip, 'method': 'UserIndexUpdated', "limit": 100, "score_address": ADDRESS['reward']}
        req = requests.get(API, params=payload)

        return json.loads(req.text)

    def _fetch_wallets_reward(self, skip: int, pool_id):
        _data = self._get_request(skip)

        for row in _data:
            block_timestamp = int(row.get("block_timestamp"))
            self.has_threshold_reach = block_timestamp <= LP_ADDED_TIMESTAMP
            print("block_timestamp", block_timestamp)
            indexed = json.loads(row.get("indexed"))
            data = json.loads(row.get("data"))
            if 'cx687fa54d7b8328fc560dc7a68a0d44d7f1091a25' == indexed[2]:
                self.wallets.append(indexed[1])

        if not self.has_threshold_reach and skip <= THRESHOLD  and len(_data)==100:
            self._fetch_wallets_reward(skip + 100, pool_id)

    def _fetch_wallets(self, skip: int, pool_id):
        _data = self._get_request(skip)

        for row in _data:
            block_timestamp = int(row.get("block_timestamp"))
            self.has_threshold_reach = block_timestamp <= LP_ADDED_TIMESTAMP

            indexed = json.loads(row.get("indexed"))
            data = json.loads(row.get("data"))
            if 'cx015c7f8884d43519aa2bcf634140bd7328730cb6' == indexed[3] and pool_id == int(data[0], 16):
                self.wallets.append(indexed[2])

        if not self.has_threshold_reach:
            self._fetch_wallets(skip + 100, pool_id)

    def get_wallets(self, pool_id):
        print("pool_id", pool_id)
        self._fetch_wallets_reward(START, pool_id)
        print(set(self.wallets))
        with open(f'{int(time.time())}-{THRESHOLD}-lp.json', 'w') as outfile:
            json.dump(list(set(self.wallets)), outfile)


if __name__ == '__main__':
    args = argumentParser()
    nid = args.nid
    token = args.token
    # print(nid, token)
    before = time.perf_counter()
    instance = LiquidityProvider()

    instance.get_wallets(OMM_sICX_POOL_ID)

