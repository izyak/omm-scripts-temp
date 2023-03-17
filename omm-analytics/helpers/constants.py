from dotenv import dotenv_values

config = dotenv_values(".env")
JSON_FILE_LOCATION = config.get("JSON_FILE_LOCATION")

ADDRESS = {
  'LENDING_POOL': 'cxcb455f26a2c01c686fa7f30e1e3661642dd53c0d',
  'OMM_TOKEN': 'cx1a29259a59f463a67bb2ef84398b30ca56b5830a',
  'DATA_PROVIDER': 'cx5f9a6ca11b2b761a469965cedab40ada9e503cb5',
  'BOOSTED_OMM': 'cxeaff5a10cb72bf85965b8b4af3e708ab772b7921',
  "OPTIMUS": ['cxa6e4587bad1d2bb4e9098ea9c19b8781b70c2ad5','cx4c18433c607bd8c6a0953e9627f5a0892ac40363','cx0cd329f5adddf9496a24f36082785582ab9aa21a']
}

TOKENS = {
  "cx2609b924e33ef00b648a409245c7ea394c467824": "sicx",
  "cxae3034235540b924dfcc1b45836c293dcc82bfb7": "iusdc",
  "cxbb2871f468a3008f80b08fdde5b8b951583acf06": "usds",
  "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": "bnusd",
  "cx1a29259a59f463a67bb2ef84398b30ca56b5830a": "omm",
  "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619": "baln",
}
# microseconds per hour
US_PER_HR = 3600_000_000
EXA = 10 ** 18
GEOMETRY_LOG_API = 'https://tracker.icon.community/api/v1/logs'
MAINNET_ENDPOINT = 'https://ctz.solidwallet.io/api/v3'
GEOMETRY_TRANSACTION_DETAIL_API = 'https://tracker.icon.community/api/v1/transactions/details/'
