import argparse
import json
import sys
import time

import requests
from checkscore.repeater import retry

LIMIT = 1000
print(sys.getrecursionlimit())
sys.setrecursionlimit(LIMIT)
print(sys.getrecursionlimit())

API = 'https://tracker.icon.community/api/v1/logs'

OMM_sICX = "cx687fa54d7b8328fc560dc7a68a0d44d7f1091a25"
OMM_USDS = "cxd5383585ecd157f0588bbf06062699126680e0f7"
OMM_IUSDC = "cx53f4dd2c3243f646b3565ecdab6f2c3b7aa6defb"
REWARD_DISTRIBUTION_CONTRACT = "cx4f2d730ad969f5c839229de42184c5e47aefef6f"

OMM_POOL_ADDRESSES = [OMM_sICX, OMM_USDS, OMM_IUSDC]

LP_ADDED_TIMESTAMP = 1629954000000000


def argumentParser():
  parser = argparse.ArgumentParser()

  parser.add_argument("-s", "--start", help="Start", type=int, default=0)

  args = parser.parse_args()

  return args


class LiquidityProvider(object):
  def __init__(self, start, threshold):
    super(LiquidityProvider, self).__init__()
    self.start = start
    self.threshold = threshold
    self.has_threshold_reach = False;
    self.wallets = []

  @retry(Exception, tries=20, delay=1, back_off=2)
  def _get_request(self, skip):
    print("skip---", skip)
    payload = {'skip': skip, 'method': 'UserIndexUpdated', "limit": 100,
               "score_address": REWARD_DISTRIBUTION_CONTRACT}
    req = requests.get(API, params=payload)

    return json.loads(req.text)

  def _fetch_wallets_reward(self, skip: int):
    _data = self._get_request(skip)

    for row in _data:
      block_timestamp = int(row.get("block_timestamp"))
      self.has_threshold_reach = block_timestamp <= LP_ADDED_TIMESTAMP
      # print("block_timestamp", block_timestamp)
      indexed = json.loads(row.get("indexed"))

      if indexed[2] in OMM_POOL_ADDRESSES:
        self.wallets.append(indexed[1])

    if not self.has_threshold_reach and skip <= self.threshold and len(
        _data) == 100:
      self._fetch_wallets_reward(skip + 100)

  def get_wallets(self):
    self._fetch_wallets_reward(self.start)
    print(set(self.wallets))
    with open(f'{int(time.time())}-{self.threshold}-lp.json', 'w') as outfile:
      json.dump(list(set(self.wallets)), outfile)


if __name__ == '__main__':
  args = argumentParser()
  start = args.start
  threshold = start + LIMIT * 100

  instance = LiquidityProvider(start, threshold)

  instance.get_wallets()
