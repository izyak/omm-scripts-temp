import argparse
import concurrent.futures
import json
import os
import time

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

NETWORK_ID = {
    "MAINNET": 1,
    "YEOUIDO": 3,
}

MAINNET_ADDRESS = {
    'LENDING_POOL': 'cxcb455f26a2c01c686fa7f30e1e3661642dd53c0d',
    'oICX': 'cx0fb973aaab3a26cc99022ba455e5bdfed1d6f0d9'
}
YEOUIDO_ADDRESS = {
    'LENDING_POOL': 'cx082dc739288fa8780998f8b1cfcd4c428c85c819',
    'oICX': 'cxc58f32a437c8e5a5fcb8129626662f2252ad2678'
}

addresses = {
    f'{NETWORK_ID["MAINNET"]}': MAINNET_ADDRESS,
    f'{NETWORK_ID["YEOUIDO"]}': YEOUIDO_ADDRESS,
}

connections = {
    f'{NETWORK_ID["MAINNET"]}': 'https://ctz.solidwallet.io',
    f'{NETWORK_ID["YEOUIDO"]}': 'https://bicon.net.solidwallet.io',
}


def argumentParser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-tkn", "--token", help="Token", type=str, default="oICX")
    parser.add_argument("-nid", "--nid", help="NID", type=int, default="1")

    args = parser.parse_args()

    return args


class TokenSnapshot(object):
    def __init__(self, nid):
        super(TokenSnapshot, self).__init__()

        self.wallets = []
        self.data = []
        server_url = connections[f'{nid}']
        self.icon_service = IconService(HTTPProvider(server_url, 3))

        self.addresses = addresses[f'{nid}']

    def _get_icx_balance(self, wallet):
        return self.icon_service.get_balance(wallet)

    def _call_tx(self, contract, method, params):
        params = {} if params is None else params
        call = CallBuilder() \
            .from_('hx91bf040426f226b3bfcd2f0b5967bbb0320525ce') \
            .to(contract) \
            .method(method) \
            .params(params) \
            .build()
        response = self.icon_service.call(call)
        return response

    def get_deposit_wallets(self):
        batch_size = 50
        index = 0
        while batch_size == 50:
            deposit_wallets = self._call_tx(self.addresses['LENDING_POOL'], 'getDepositWallets', {'_index': index})
            self.wallets.extend(deposit_wallets)
            index += 1
            batch_size = len(deposit_wallets)
        deposit_wallets = self._call_tx(self.addresses['LENDING_POOL'], 'getDepositWallets', {'_index': index})
        self.wallets.extend(deposit_wallets)

    def snapshot(self, _token):
        self.token = _token
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 20)) as executor:
            executor.map(self._get_balances, self.wallets)
        _data = self._get_data()
        _sum = 0
        for item in _data:
            print(item['balance'])
            _sum += item['balance']

        print(f"The sum of {_token} balances is: {_sum}")

        with open(f'{int(time.time())}_{token}-holders.json', 'w') as outfile:
            json.dump(_data, outfile)

    def _get_balances(self, wallet):
        _token_address = self.addresses[self.token]
        _balance = self._call_tx(_token_address, 'balanceOf', {'_owner': wallet})
        _balance = int(_balance, 16) / 10 ** 18
        if _balance > 0:
            _principalBalances = self._call_tx(_token_address, 'principalBalanceOf', {'_user': wallet})
            _row = {
                "wallet": wallet,
                "principal_balance": int(_principalBalances, 16) / 10 ** 18,
                "balance": _balance
            }
            self.data.append(_row)

    def _get_data(self):
        return sorted(self.data, reverse=True, key=lambda _row: _row['balance'])


if __name__ == '__main__':
    args = argumentParser()
    nid = args.nid
    token = args.token
    print(nid, token)
    before = time.perf_counter()
    instance = TokenSnapshot(nid)

    instance.get_deposit_wallets()

    after = time.perf_counter()
    print(f"The time taken to fetch wallets: {after - before} seconds")

    instance.snapshot(token)

    after = time.perf_counter()
    print(f"The time taken to calculate: {after - before} seconds")
