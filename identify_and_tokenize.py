"""Identifies and tokenizes interesting equations.

A script to run from the command line that can identify interesting equations
and tokenize them.
"""
import pandas as pd
from common.clean import replace
from common.heuristics import test_for_suitable, split_high_level_eqs
from common.tokenize import tokenize
import sys
<<<<<<< HEAD
import csv


def process_row(r, writer, sw=['\\', '\\\\']):
    r.append(replace(r[1]))
    r.append(split_high_level_eqs(r[2]))

    if r[3] is None or len(r[3]) < 2:
        return
    suitable = test_for_suitable(r[3])
    if suitable is None:
        return
    r.append(suitable)
    r.append([tokenize(e, sw) for e in r[4]])

    writer.writerow(row)
=======
>>>>>>> 5a0c4835b9b127afbb543b8ead1f48f23f3f482c

# test: "../data/eqs_100k.tsv" 'aligned_ex.csv'
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python identify_and_tokenize.py /path/to/tsv outpath/filename.csv")
    else:
        filename = sys.argv[1]
        outpath = sys.argv[2]
<<<<<<< HEAD

    with open(filename) as csvfile:
        with open(outpath, "w+") as outfile:
            reader = csv.reader(csvfile, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t')
            for i, row in enumerate(reader):
                if i == 0:
                    writer.writerow(['eq_id', 'eq', 'clean', 'clean_split',
                    'clean_split_filtered', 'clean_split_filtered_tokenized'])
                process_row(row, writer)

                if i % 100000 == 0:
                    print("{i} rows processed".format(i=i))
=======
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
>>>>>>> 5a0c4835b9b127afbb543b8ead1f48f23f3f482c
