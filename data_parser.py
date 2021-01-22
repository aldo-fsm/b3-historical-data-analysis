import re
from typing import BinaryIO
import pandas as pd
from pandas.core.frame import DataFrame
from tqdm import tqdm

PARSE_TABLE = pd.read_csv('datasets/parse-table.csv')
FIELDS_TYPES_MAPPING = dict(
    dateFields=['DATA','DATVEN'],
    intFields=['PRAZOT','TOTNEG','QUATOT','FATCOT'],
    floatFields=['PREABE','PREMAX','PREMIN','PREMED','PREULT','PREOFC','PREOFV','VOLTOT','PREEXE','PTOEXE'],
    stringFields=['TIPREG','CODBDI','CODNEG','TPMERC','NOMRES','ESPECI','MODREF','INDOPC','CODISI','DISMES'],
)

def parseRecord(line: str):
    data = {
        row.fieldName : parseField(row.fieldName, row.type, line[int(row.startPos)-1:int(row.endPos)])
        for i, row in PARSE_TABLE.iterrows()
    }
    return data

def parseField(fieldName: str, fieldType: str, value: str):
    if fieldName in FIELDS_TYPES_MAPPING['dateFields']:
        return parseDate(value)
    elif fieldName in FIELDS_TYPES_MAPPING['intFields']:
        try:
            return int(value)
        except:
            return None
    elif fieldName in FIELDS_TYPES_MAPPING['floatFields']:
        integerDigitNumber = int(re.findall('\((\d+)\)', fieldType)[0])
        return float(f'{value[:integerDigitNumber]}.{value[integerDigitNumber:]}')
    return value.strip()

def parseDate(date: str):
    return f"{date[0:4]}-{date[4:6]}-{date[6:8]}"

def parseDataset(file: BinaryIO) -> DataFrame:
    records = []
    for line in tqdm(file.readlines()):
        if line[:2] == '00': continue
        if line[:2] == '99': break
        records.append(
            parseRecord(line)
        )
    print('aaaa')
    return pd.DataFrame(records)
