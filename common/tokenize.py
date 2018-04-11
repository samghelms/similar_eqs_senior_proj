import re


def empty(s):
    """a set of rules to find empty strings"""
    s = s.strip()
    s = s.strip("\\")
    return True if s == "" else False


def break_rule(c, state):
    if state == 'macro':
        if re.match('[A-Za-z]', c):
            return 'append'
        else:
            return 'new'
    if state == 'num_or_var_or_op': return 'new'
    return 'none'


def update_state(c, state):
    if state in ['macro', 'start'] and re.match('[A-Za-z]', c) or c == '\\':
        return 'macro'
    if re.match('[A-Za-z0-9{}()\*+\-=]', c): return 'num_or_var_or_op'
    if re.match('\s', c): return 'space'
    return 'unknown'


def tokenize(s, stop_words):
    cur = 'START'
    ret = []
    state = 'start'
    for c in s:
        state = update_state(c, state)
        decision = break_rule(c, state)
        if decision == 'new':
            if cur not in stop_words:
                ret.append(cur)
            cur = c
        elif decision == 'append':
            cur += c
    if cur != '':
        ret.append(cur)
    return ret
