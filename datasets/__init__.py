import pandas as pd
import dask.dataframe as dd
import os

DATASETS_DIR = 'datasets'

def getDatasetName(year: int) -> str:
    return f'COTAHIST_A{year}'

def loadDataset(datasetName: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATASETS_DIR, f'{datasetName}.csv'))

def loadDaskDataset(datasetName: str) -> dd.DataFrame:
    return dd.read_csv(os.path.join(DATASETS_DIR, f'{datasetName}.csv'), parse_dates = ["DATA"])

def loadDaskFullDataset():
    return loadDaskDataset('*')