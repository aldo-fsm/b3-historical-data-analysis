import streamlit as st
import pandas as pd
import re

with open('datasets/raw/COTAHIST_A2019.TXT') as f:
    text = f.read()

parseTable = pd.read_csv('datasets/parse-table.csv')

allLines = text.split('\n')
allLines[:10]
allLines = allLines[1:-2]
st.write(
    len(allLines),
    parseTable
)
# st.write(
#     ([(i, line) for (i, line) in enumerate(allLines) if '99' in line[:2]]),
#     ([(i, line) for (i, line) in enumerate(allLines) if '00' in line[:2]])
# )
def parseRecord(line: str):
    data = {
        row.fieldName : parseField(row.fieldName, row.type, line[int(row.startPos)-1:int(row.endPos)])
        for i, row in parseTable.iterrows()
    }
    # data['DATA'] = parseDate(data['DATA'])
    return data

fieldsTypesMapping = dict(
    dateFields=['DATA','DATVEN'],
    intFields=['PRAZOT','TOTNEG','QUATOT','FATCOT'],
    floatFields=['PREABE','PREMAX','PREMIN','PREMED','PREULT','PREOFC','PREOFV','VOLTOT','PREEXE','PTOEXE'],
    stringFields=['TIPREG','CODBDI','CODNEG','TPMERC','NOMRES','ESPECI','MODREF','INDOPC','CODISI','DISMES'],
)

def parseField(fieldName: str, fieldType: str, value: str):
    if fieldName in fieldsTypesMapping['dateFields']:
        return parseDate(value)
    elif fieldName in fieldsTypesMapping['intFields']:
        try:
            return int(value)
        except:
            return None
    elif fieldName in fieldsTypesMapping['floatFields']:
        integerDigitNumber = int(re.findall('\((\d+)\)', fieldType)[0])
        return float(f'{value[:integerDigitNumber]}.{value[integerDigitNumber:]}')
    return value.strip()

def parseDate(date: str):
    return f"{date[0:4]}-{date[4:6]}-{date[6:8]}"

st.write(
    [parseRecord(line) for line in allLines[:5]]
)