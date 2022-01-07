import requests
import streamlit as st
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
import plotly_express as px

# https://github.com/binance/binance-spot-api-docs
# https://python-binance.readthedocs.io/en/latest/
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
client = Client()

@st.cache()
def getKlines():
    print('getting klines')
    klines = client.get_historical_klines("BTCUSDC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    columns = [
        'open_time',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'close_time',
        'quote_asset_volume',
        'number_of_trades',
        'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume',
        'Ignore.',
    ]
    return pd.DataFrame(klines, columns=columns).astype(float)
klines = getKlines()
# klines
st.write(
    px.line(klines, x='close_time', y='close')
)

@st.cache()
def getAllAssets():
    all_assets = requests.get('https://www.binance.com/bapi/asset/v2/public/asset/asset/get-all-asset').json()['data']
    return all_assets

all_assets = getAllAssets()
stablecoins = set(
    [coin['assetCode'] for coin in all_assets if 'stablecoin' in coin['tags']] +
    ['USDT', 'USDC', 'BUSD', 'UST', 'DAI', 'TUSD', 'USDP', 'USDN', 'FEI', 'RSR']
)
st.write(stablecoins)

st.markdown('---')
# ======== coin gecko ========

VS_CURRENCY='usd'

api = CoinGeckoAPI()

@st.cache()
def getMarkets():
    return api.get_coins_markets(VS_CURRENCY, order='volume_desc')

@st.cache()
def getCoinList():
    return api.get_coins_list()

coinList = pd.DataFrame(getCoinList())
coinList

markets = pd.DataFrame(getMarkets())
markets['symbol'] = markets['symbol'].apply(lambda symbol: symbol.upper())
markets = markets[~markets['symbol'].isin(stablecoins)]
markets = markets.sort_values(by='total_volume', ascending=False)
markets

st.write(
    px.bar(markets.head(10), x='symbol', y='total_volume')
)
