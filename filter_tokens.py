"""Filter tokens with a stoplist of prefixes and tokens."""
import json

def _remove_following_n(tokens, i, close_toks):
    orig = i
    for t in tokens:
        i += 1
        if t in close_toks:
            break
    return i if (i - orig) > 3 else orig # don't skip small sub expressions, in case someone is creating a symbol (common)

def filter_tokens(tokens,
                  tokens_to_filter=['\\begin', '\\end', '\\mbox',
                                    '\\text', '\\textrm',
                                    '\\textstyle', '\\hbox'],
                  open_toks=json.load(open('data/open_list.json')) + ['{'],
                  close_toks=json.load(open('data/close_list.json')) + ['}']):
    """
    @ param tokens: list of tokens (strings)
    @ param tokens_to_filter: tokens to filter, list, default above
    """
    filtered = []
    filt = False
    skip_to = 0
    for i, t in enumerate(tokens):
        if i < skip_to:
            continue

        if t in tokens_to_filter:
            if i < len(tokens) - 1 and tokens[i+1] in open_toks:
                skip_to = _remove_following_n(tokens[i+1:], i+1, close_toks)
        if skip_to <= i+1:
            filtered.append(t)
    return filtered
