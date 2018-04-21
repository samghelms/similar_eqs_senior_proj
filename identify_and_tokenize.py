"""Identifies and tokenizes interesting equations.

A script to run from the command line that can identify interesting equations
and tokenize them.
"""
import pandas as pd
from common.clean import replace
from common.heuristics import test_for_suitable, split_high_level_eqs
from common.tokenize import tokenize
import sys
import csv
import json

def process_row(r, writer, sw=['\\', '\\\\']):
    d = {}
    d['eq_id'] = r[0]
    d['eq'] = r[1]
    d['clean'] = replace(r[1])
    d['clean_split'] = split_high_level_eqs(d['clean'])
    if d['clean_split'] is None or len(d['clean_split']) < 2:
        return
    suitable = test_for_suitable(d['clean_split'])
    if suitable is None:
        return
    d['clean_split_filtered'] = suitable
    d['clean_split_filtered_tokenized'] = [tokenize(e, sw) for e in d['clean_split_filtered']]
    writer.write(json.dumps(d)+'\n')

# test: "../data/eqs_100k.tsv" 'aligned_ex.csv'
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python identify_and_tokenize.py /path/to/tsv outpath/filename.csv")
    else:
        filename = sys.argv[1]
        outpath = sys.argv[2]

    with open(filename, 'r') as csvfile:
        with open(outpath, "w+") as outfile:
            reader = csvfile #csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL, delimiter='\t') 
            for i, row in enumerate(reader):
                row = row.split('\t', 1)
                if i == 0:
                    continue
                process_row(row, outfile)

                if i % 100000 == 0:
                    print("{i} rows processed".format(i=i))
