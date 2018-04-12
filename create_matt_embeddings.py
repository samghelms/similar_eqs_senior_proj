import pandas as pd
import ast
from modules.ibm_eqs.vocab import Vocab
from modules.ibm_eqs.tr_embed import TREmbed

if __name__ == '__main__':
    df = pd.read_csv('first_1m_processed.csv')
    df['clean_split_filtered_tokenized']= df['clean_split_filtered_tokenized'].apply(ast.literal_eval)
    df_len2_subset = df[df['clean_split_filtered_tokenized'].apply(len) == 2]
    eqs = df_len2_subset['clean_split_filtered_tokenized'].tolist()
    eqs = [(sublist[0], sublist[1]) for sublist in eqs]
    print("{num} equations detected".format(num=len(eqs)))

    v2 = Vocab(eqs)
    print("constructing")
    tre = TREmbed(v2, v2.transform(eqs))
    tre.estimate()

    embeds = tre.construct_embeds([f for e, f in eqs], k=200)
