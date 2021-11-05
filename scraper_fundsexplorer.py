import streamlit as st
# -----

import requests
from bs4 import BeautifulSoup
import json

FULL_MONTHS = {'janeiro': 1,  'fevereiro': 2, u'março': 3,    'abril': 4,
               'maio': 5,     'junho': 6,     'julho': 7,     'agosto': 8,
               'setembro': 9, 'outubro': 10,  'novembro': 11, 'dezembro': 12}

BASE_URL = 'https://www.fundsexplorer.com.br/funds'

def getUrl(ticker):
    return f'{BASE_URL}/{ticker}'

@st.cache()
def getData(ticker):
    print('oi3')
    url = getUrl(ticker)
    html = requests.get(url).content
    return html

soup = BeautifulSoup(getData('irdm11'))

def extractChartData(chartWrapperId):
    chartWrapper = soup.find(attrs=dict(id=chartWrapperId))
    script = chartWrapper.find('script')
    scriptContent = script.contents[0]
    data = json.loads(scriptContent.split('data: ')[1].split(', options:')[0])
    return data

dividendData = extractChartData('dividends-chart-wrapper')
yieldData = extractChartData('yields-chart-wrapper')

st.write(
    dividendData,
    yieldData
)