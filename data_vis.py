import streamlit as st
import plotly_express as px

from datetime import datetime
from datasets import loadDaskDataset, loadDataset, getDatasetName

def load():
    time = datetime.now()
    st.write(f'{time} - loading dataset...')
    dataset = loadDaskDataset(
        getDatasetName(2020)
    )
    time2 = datetime.now()
    st.write(f'{time2} - loading finished')
    st.write('Load time:', time2-time)
    return dataset 

dataset = load()

st.write(
    # dataset.size.compute(),
    dataset.head(),
    dataset[dataset.CODNEG == 'ABBV3'].head()
)

tickers = st.multiselect('CODNEG', dataset.CODNEG.unique().compute())
st.write(
    px.line(dataset[dataset.CODNEG.isin(tickers)].compute().sort_values('DATA'), x='DATA', y='PREABE', color='CODNEG')
)