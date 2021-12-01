import streamlit as st
from scrapping import scraper_fundsexplorer
import pandas as pd
import numpy as np
import plotly_express as px

@st.cache()
def getData():
    fiis = pd.read_csv('datasets/fii.csv', delimiter=';')

    tickers = fiis['Código do fundo']

    dividends, yields = scraper_fundsexplorer.extractAll(tickers, './datasets')
    return fiis, dividends, yields

fiis, dividends, yields = getData()
fiis = fiis.copy()

fiis['liquidez'] = fiis.apply(lambda row: row['Preço Atual'] * row['Liquidez Diária'], axis=1)

fiis['yields'] = fiis['Código do fundo'].apply(lambda ticker: yields[yields.ticker == ticker].value.values.T)
fiis['yieldsDates'] = fiis['Código do fundo'].apply(lambda ticker: yields[yields.ticker == ticker].date.values.T)

MAX_NUM_MONTHS = 24
fiis['yields'] = fiis.yields.apply(lambda yields: yields[-MAX_NUM_MONTHS:])
fiis['yieldsDates'] = fiis.yieldsDates.apply(lambda yieldsDates: yieldsDates[-MAX_NUM_MONTHS:])

fiis['yieldMean'] = fiis.yields.apply(lambda data: data.mean())
fiis['yieldMedian'] = fiis.yields.apply(lambda data: np.median(data))
fiis['yieldStd'] = fiis.yields.apply(lambda data: data.std())
fiis['meanMedianDiscrepance'] = fiis.apply(lambda row: np.abs(row.yieldMedian - row.yieldMean)/row.yieldMedian, axis=1)

fiis['numYieldDataPoints'] = fiis.yields.apply(lambda data: len(data))
fiis['yearsOfData'] = fiis.yields.apply(lambda data: len(data)/12)


fiis

st.write(
    fiis.Setor.value_counts(),
)

# # 1
#     - filtrar:
#       - liquidez >= R$ 200.000
#       - tipo != incorporação ou desenvolvimento
#       - baixa discrepância entre média e mediana do DY
#       - existem a pelo menos 1 ano
# # 2
#     - Somar posição nos dois rankings:
#       - Ranking P/VPA (asc)
#       - Ranking mediana DY (desc)
# # 3
#     - S-Rank
#       - ordenar pela soma da etapa 2 (asc)

filtered = fiis.copy()
filtered = filtered[filtered.liquidez >= 200000] # liquidez >= R$ 200.000
filtered = filtered[filtered.meanMedianDiscrepance <= 0.1] # baixa discrepância entre média e mediana do DY
filtered = filtered[filtered.numYieldDataPoints >= 12] # pelo menos 1 ano de dados dividend yield

filtered = filtered[filtered['Quantidade Ativos'] > 1]

filtered['pvpaRankPosition'] = np.argsort(np.argsort(filtered['P/VPA'].values))
filtered['yieldMedianRankPosition'] = np.argsort(np.argsort(-filtered.yieldMedian.values))
filtered['srankPosition'] = filtered.apply(lambda row: row.pvpaRankPosition + row.yieldMedianRankPosition, axis=1)

ranked = filtered.sort_values('srankPosition')

st.write(
    fiis.shape,
    filtered.shape,
    ranked,
)

ranked['negYieldMedian'] = -ranked.yieldMedian
st.write(
    px.scatter(ranked, x = 'P/VPA', y = 'negYieldMedian', hover_name='Código do fundo')
)
