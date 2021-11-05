import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm import tqdm

BASE_URL = 'https://www.fundsexplorer.com.br/funds'

def getUrl(ticker):
    return f'{BASE_URL}/{ticker}'

def getPage(ticker):
    url = getUrl(ticker)
    html = requests.get(url).content
    return html

def extractChartData(soup, chartWrapperId):
    chartWrapper = soup.find(attrs=dict(id=chartWrapperId))
    scripts = chartWrapper.find_all('script')
    script = [script for script in scripts if script.text][0]
    scriptContent = script.text
    data = json.loads(scriptContent.split('data: ')[1].split(', options:')[0])
    return dict(
        labels=data['labels'],
        data=data['datasets'][0]['data']
    )

def extractData(ticker):
    html = getPage(ticker)
    soup = BeautifulSoup(html)

    dividendData = extractChartData(soup, 'dividends-chart-wrapper')
    yieldData = extractChartData(soup, 'yields-chart-wrapper')
    return dividendData, yieldData

def tryGetDataset(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(dict(
            ticker=[],
            date=[],
            value=[],
        ))

def extractAll(tickers, targetDir='./'):
    dividendDatasetPath = f'{targetDir}/fii_dividends_hist.csv'
    yieldDatasetPath = f'{targetDir}/fii_yields_hist.csv'
    dividendDf = tryGetDataset(dividendDatasetPath)
    yieldDf = tryGetDataset(yieldDatasetPath)
    for ticker in tqdm(tickers):
        if ticker in yieldDf.ticker.values:
            continue
        try:
            dividendData, yieldData = extractData(ticker)
            dividendDf = pd.concat([
                dividendDf,
                pd.DataFrame(dict(
                    ticker=ticker,
                    date=dividendData['labels'],
                    value=dividendData['data'],
                ))
            ])
            yieldDf = pd.concat([
                yieldDf,
                pd.DataFrame(dict(
                    ticker=ticker,
                    date=yieldData['labels'],
                    value=yieldData['data'],
                ))
            ])
            dividendDf.to_csv(dividendDatasetPath, index=False)
            yieldDf.to_csv(yieldDatasetPath, index=False)
        except Exception as e:
            print(ticker)
            raise(e)

    return dividendDf, yieldDf