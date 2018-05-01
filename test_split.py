from split import split_high_level_eqs, split_exprs, split
from tok import tokenize_and_fix_macros

def test_split_high_level_eqs():
	s = '\int_0^{\infty}\\frac{r^{2n-3}dr}{(1+r^2)^{2n-1}}  =  \\frac{1}{2}\int_0^{\infty}\\frac{r^{n-2}dr}{(1+r)^{2n-1}}  =  \\frac{1}{2n-2} {2n-2 \choose n-1}^{-1}'
	tok = tokenize_and_fix_macros(s)
	spl = split_high_level_eqs(tok)
	assert len(spl) == 3


def test_split_exprs():
	s = '\int_0^{\infty}\\frac{r^{2n-3}dr}{(1+r^2)^{2n-1}}  =  \\frac{1}{2}\int_0^{\infty}\\frac{r^{n-2}dr}{(1+r)^{2n-1}}  =  \\frac{1}{2n-2} {2n-2 \choose n-1}^{-1}'
	tok = tokenize_and_fix_macros(s)
	spl = split_exprs(tok)
	# print(spl)
	assert len(spl) == 1

	spl = split_exprs(tokenize_and_fix_macros("5 \\\\ 6"))

	assert spl == [['5'], ['6']]

	spl = split_exprs(tokenize_and_fix_macros("5 = 6 \\\\ = 6 + 7"))
	assert spl == [['5', '=', '6', '=', '6', '+', '7']]

	spl = split_exprs(tokenize_and_fix_macros("5 = 6 \\text{ and } 6 + 7 = 6"))
	assert [['5', '=', '6'], ['6', '+', '7', '=', '6']] == spl

def test_split():
	spl = split(tokenize_and_fix_macros("5 = 6 \\\\ = 6 + 7"))
	assert spl == [[['5'], ['6'], ['6', '+', '7']]]

	s = '\int_0^{\infty}\\frac{r^{2n-3}dr}{(1+r^2)^{2n-1}}  =  \\frac{1}{2}\int_0^{\infty}\\frac{r^{n-2}dr}{(1+r)^{2n-1}}  =  \\frac{1}{2n-2} {2n-2 \choose n-1}^{-1}'
	tok = tokenize_and_fix_macros(s)
	spl = split(tok)

	assert len(spl) == 1 and len(spl[0]) == 3
