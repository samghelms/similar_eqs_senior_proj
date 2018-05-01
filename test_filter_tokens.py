from filter_tokens import filter_tokens

def test_filter_tokens():
	filtd = (filter_tokens(['\\int', '\\text', '{', 'x', '}', '\\text', '{', 'h', 'i', 't', 'h', 'e', 'r', 'e', '}', 'x', '+', 'y']))
	assert filtd == ['\\int', '\\text', '{', 'x', '}', 'x', '+', 'y']

	s = "b_1(u) = \\frac{1 - u q^{1/2} }{1 - u q^{-1/2}} \mbox{ and }b_2(u) = \\frac{ -uq^{-1/2}+ q^{-1}}{ 1 - uq^{-1/2}}."