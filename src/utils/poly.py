# polynomial operations
from .util import *


def poly_mod(exp):
    """
    expression (mod (x^f + 1))
    """
    m = len(exp) - 1
    res = exp % p
    for i in range(0, m-f+1):
        d = res[i]
        res[i] -= d
        res[i + f] -= d
    res = res[-f:]
    return vector_to_Rp(res)


def poly_op(a, s1, s2):
    """
    t = a * s1 + s2
    """
    return poly_mod(np.polyadd(np.convolve(s1, a), s2))


# def poly_mod(exp):
#     """
#     expression (mod (x^f + 1))
#     """
#     ideal = [1] + (f - 1) * [0] + [1]
#     ideal = sp.Poly(ideal, sp.symbols('x'))
#     exp = sp.Poly(exp, sp.symbols('x'))
#     q, r = sp.div(exp, ideal)
#     # mod_output = int_cast(np.polydiv(exp, ideal)[1])
#     mod_output = np.array(r.all_coeffs())
#     mod_output = np.pad(mod_output, (f - len(mod_output), 0))
#     return vector_to_Rp(mod_output)
