from tok import tokenize, fix_macros, tokenize_and_fix_macros

def test_tokenize():
	toks = tokenize('\\frac{x} {y} \\begin{eq }x = \\textfadfsad{tets} \\int 1.0 .6 \\end{test}')
	assert toks == ['\\frac', '{', 'x', '}', '{', 'y', '}', '\\begin', '{', 'e', 'q', '}', 'x', '=', '\\textfadfsad', '{', 't', 'e', 't', 's', '}', '\\int', '1.0', '.6', '\\end', '{', 't', 'e', 's', 't', '}']

	toks = tokenize('4 \\\\ 4')
	assert len(toks) == 3

def test_fix_macros():
	toks = tokenize('\\frac{x} {y} \\begin{eq }x = \\textfadfsad{tets} \\int 1.0 .6 \\end{test}')
	fixed = fix_macros(toks, debug=True)
	assert fixed == ['\\frac', '{', 'x', '}', '{', 'y', '}', '\\begin', '{', 'e', 'q', '}', 'x', '=', '\\text', 'fadfsad', '{', 't', 'e', 't', 's', '}', '\\int', '1.0', '.6', '\\end', '{', 't', 'e', 's', 't', '}']

def test_tokenize_and_fix_macros():
	s = '\\frac{x} {y} \\begin{eq }x = \\textfadfsad{tets} \\int 1.0 .6 \\end{test}'
	toks = tokenize(s)
	fixed = fix_macros(toks, debug=True)

	assert fixed == tokenize_and_fix_macros(s)
