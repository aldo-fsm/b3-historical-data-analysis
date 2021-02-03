import pandas as pd

def getDatasetName(year: int) -> str:
    return f'COTAHIST_A{year}'

def loadDataset(datasetName: str) -> pd.DataFrame:
    return pd.read_csv(f'./{datasetName}.csv')