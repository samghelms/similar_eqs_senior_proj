# from vocab import Vocab
# from tr_embed import TREmbed
# import pandas as pd
# from numba import jit
# import numpy as np
# import time

# def read_eqs(fname):
#     import pandas as pd
#     import ast

#     df = pd.read_csv(fname, header=None)

#     df[1] = df[1].apply(ast.literal_eval)

#     df_len2_subset = df[df[1].apply(len) == 2]
#     return [(sublist[0], sublist[1]) for sublist in df_len2_subset[1].tolist()] # the list of tokenized aligned equations.

# def flatten(li):
#     return [item for sublist in li for item in sublist]

# if __name__ == '__main__':
#     # d = [(['test', 'y'], ['testito', 'x']),
#     #      (['test', 'u'], ['testito', 'p'])]
#     # print(d)
#     # v = Vocab(d)

#     # print(v.e_d)
#     # print(v.f_d)
#     # print(v.etoint('test'))
#     # print(v.transform(d))

#     eqs = read_eqs('data/aligned_ex.csv')[0:1000]
#     v2 = Vocab(eqs)
#     print("constructing")
#     tre = TREmbed(v2, v2.transform(eqs))
#     # print(tre.cur_log_lik)
#     tre.estimate()
#     # print(v2.f_d)
#     # print([f for e, f in eqs])
#     # print(tre.construct_embeds([f for e, f in eqs]))

#     # embeds = {}
#     # for inp_str in src_eqs:
#     #     embeds[inp_str] = tre.embed(tokenize(inp_str))
