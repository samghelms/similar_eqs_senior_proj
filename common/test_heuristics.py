from heuristics import (split_high_level_eqs,
                        high_level_eq_test,
                        has_op,
                        test_high_level_only)


def test_split_high_level_eqs():
    # tests
    print(split_high_level_eqs("x = y"))
    print(split_high_level_eqs(r"\frac{x=y}{1=y} = y"))
    print(split_high_level_eqs(r"\frac{x=y}{1=y = y"))
    print(split_high_level_eqs('\\alpha=\\frac{1}{\\sum_{i=1}^{k}1/d_i}=\\alpha=\\frac{1}{\\sum_{i=1}^{k}1/d_i}'))


def test_high_level_eq_test():
    raise NotImplentedError

def test_has_op():
    print(has_op('7+5'))
    print(has_op(r'\bigwedge7'))
    print(has_op(r'\igwedge7'))
    print(has_op(r''))

def test_high_level_only():
    print (high_level_only("\int{xfdf} x = y"))
    print (high_level_only("\int{xfdf} x_y = y"))
