# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 10:19:10 2020

@author: Daniel Filler
"""

from pandas import DataFrame, read_csv
import torch
from transformers import BertTokenizer, BertModel

data = read_csv('fxpfinal.csv', encoding='cp1255')
print("data loaded")
data = data['post'].str.replace('\n', ' ').str.replace('\r', ' ').values.tolist()
print("removed whitespaces")

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
print("loaded tokenizer")
print("tokenization started")
tokenized_text = tokenizer.tokenize(data)
print("tokenization ended")