from data_parser import parseDataset
import streamlit as st
import pandas as pd
import re

with open('datasets/raw/COTAHIST_A2019.TXT') as f:
    print('start')
    df = parseDataset(f)
    print('fim')
