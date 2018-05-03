import json

def split_exprs(tokens, 
                l_dep_tokens=json.load(open('data/open_list.json')) + ['{'],
                r_dep_tokens=json.load(open('data/close_list.json')) + ['}'],
                break_tokens=json.load(open('data/punctuation_list.json')),
                relations_list=json.load(open('data/relations_list.json')),
                text_tol = 4):
    """@param: tokens: a list of tokens to split up
       @param: l_dep_tokens: tokens that signify entering into a dependent. Default from KaTeX
       @param: r_dep_tokens: tokens that signify exiting a dependent. Default from KaTeX
       @param: break tokens: tokens like , and ; that should be broken on. Default from KaTeX
       @param: text_tol: how many tokens to allow in a text tag before splitting
        @returns a list of lists of tokens from seperate subexpressions.
        Deals with, for example, aligned equations where the first line is
        something like f = x + y and the second line is g = 6 + i, which should
        not be considered aligned. It will consider f(x) = y \\ = y + 8 a single expression, however
        """
    dep_depth = 0
    prev_idx = 0
    ret = [[]]
    i = 0
    skip = 0
    for i, t in enumerate(tokens):
        if i < skip:
            continue
        if t in l_dep_tokens:
            dep_depth += 1
        elif t in r_dep_tokens:
            dep_depth -= 1
        elif dep_depth == 0:
            if t == '\\\\':
                # folds in lines that are a continuation
                if i < len(tokens) - 1 and tokens[i+1] in relations_list:
                    skip = i + 1
                # otherwise it splits
                else:
                    ret.append([])
                    skip = i + 1
            elif t in break_tokens:
                skip = i + 1
                ret.append([])
            # handle inline text
            elif t in ['\\mbox', '\\text', '\\textrm', '\\textstyle', '\\hbox']:
                skip = i
                for _t in tokens[i:]:
                    skip += 1
                    if _t in r_dep_tokens:
                        break
                if skip - i > text_tol:
                    ret.append([])
                else:
                    skip = i

        if i >= skip:
            ret[-1].append(t)

    return ret

def split_high_level_eqs(tokens,
                         l_dep_tokens=json.load(open('data/open_list.json')) + ['{'], 
                         r_dep_tokens=json.load(open('data/close_list.json')) + ['}'],
                         split_tokens=json.load(open('data/relations_list.json'))):
    """@param: tokens: list of strings
       @param: l_dep_tokens: characters that signify entering into a dependent. Default from KaTeX
       @param: r_dep_tokens: characters that signify exiting a dependent. Default from KaTeX
       @param: split_tokens: characters that signify exiting a dependent. Default from KaTeX
      @returns list of lists of strings split on split_chars"""
    dep_depth = 0
    prev_idx = 0
    ret = []
    i = 0
    for t in tokens:
        if t in l_dep_tokens:
            dep_depth += 1
        elif t in r_dep_tokens:
            dep_depth -= 1
        elif t in split_tokens:
            if dep_depth == 0:
                ret.append(tokens[prev_idx:i])
                prev_idx = i + 1
        i += 1
    if (prev_idx < i):
        ret.append(tokens[prev_idx:])
    if(dep_depth != 0):
        return []

    return ret

def split(tokens):
    """Wrapper for both splits.
    @param tokens: list of tokens
    return a list of lists of epxressions and tokens"""
    return [split_high_level_eqs(eq) for eq in split_exprs(tokens)]