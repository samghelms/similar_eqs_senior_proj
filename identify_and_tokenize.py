"""Identifies and tokenizes interesting equations.

A script to run from the command line that can identify interesting equations
and tokenize them.
"""
import pandas as pd
from common.clean import replace
from common.heuristics import test_for_suitable, split_high_level_eqs
from common.tokenize import tokenize
import sys

# test: "../data/eqs_100k.tsv" 'aligned_ex.csv'
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python identify_and_tokenize.py /path/to/tsv outpath/filename.csv")
    else:
        filename = sys.argv[1]
        outpath = sys.argv[2]
    df = pd.DataFrame(pd.read_csv(filename, sep="\t",
                                  header=None))
    print("loaded")
    # stopwords
    sw = ['\\', '\\\\']
    df.columns = ["eq_id", "eq"]
    df['clean'] = replace(df['eq'])
    df['clean_split'] = df['clean'].apply(split_high_level_eqs)
    se = df['clean_split'].apply(lambda x: len(x) > 1 if x is not None
                                 else False)
    print("cleaned and split")
    df = df[se].reset_index()
    se = df['clean_split'].apply(test_for_suitable)
    df['clean_split_filtered'] = se
    filt = df['clean_split_filtered'].apply(lambda x: x is not None)
    print("applied filter")
    df = df[filt]
    df['clean_split_filtered_tokenized'] = df['clean_split_filtered'].apply(lambda x: [tokenize(e, sw) for e in x])
    print("writing")
    df.to_csv(outpath)
