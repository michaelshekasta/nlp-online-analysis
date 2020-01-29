# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 10:19:10 2020

@author: Daniel Filler
"""

from pandas import DataFrame, read_csv
import torch
from transformers import BertTokenizer, BertModel, BertEncoder

data = read_csv('fxpfinal.csv', encoding='cp1255')
data = data['post'].str.replace('\n', ' ').str.replace('\r', ' ').squeeze()

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
tokenized_text = tokenizer.tokenize(data)
