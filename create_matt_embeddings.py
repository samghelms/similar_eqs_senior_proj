import pandas as pd
import ast
from modules.ibm_eqs.vocab import Vocab
from modules.ibm_eqs.tr_embed import TREmbed
import sys
import csv
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python create_matt_embeddings.py /path/to/source/csv")
        exit()
    eqs = []
    filename = sys.argv[1]
    with open(filename, 'r') as infile:
        for i, line in enumerate(infile):
            try:
                line = json.loads(line)         
            except:
                continue
            line_len = len(line['clean_split_filtered_tokenized'])
            if line_len == 2:
                eqs.append((line['clean_split_filtered_tokenized'][0], line['clean_split_filtered_tokenized'][1]))
            if i == 1000000:
                break 
    print("read all lines")
    print("{num} equations detected".format(num=len(eqs)))
    v2 = Vocab(eqs)
    print("constructing")
    tre = TREmbed(v2, v2.transform(eqs))
    tre.estimate()
    embeds = tre.construct_embeds([f for e, f in eqs], k=200)
