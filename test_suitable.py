from suitable import count_vars, count_ops, suitable

def test_count_vars():
	assert count_vars(['x', '1.0', '900']) == 3

	assert count_vars(['x', '1.0', '900', '\\theta']) == 4

	assert count_vars(['x', '1.0', '900', '\\theta', '\\int']) == 5

def test_count_ops():
	assert count_ops(['x', '+', '1.0', '900', '\\theta', '\\int']) == 1

def test_test_for_suitable():
	toks = ['x', '+', '1.0', '900', '\\theta', '\\int']
	assert suitable(toks)