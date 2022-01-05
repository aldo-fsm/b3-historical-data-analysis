import streamlit as st
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
import plotly_express as px

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
client = Client()

# get market depth
# depth = client.get_order_book(symbol='BNBBTC')

# get all symbol prices
# prices = client.get_all_tickers()

# fetch 1 minute klines for the last day up until now
klines = client.get_historical_klines("BTCUSDC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
st.write(klines[:3])
kla = np.array(klines).astype(float)
# series = pd.Series(klines)
# series
# st.write(
#     px.line(series)
# )

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
markets


st.write(
    px.bar(markets, y='symbol', x='total_volume' )
)
