import os
import sys
import unittest

sys.path.append( os.path.join('..', 'leastfun'))
from proc.least import *

varlist = ['x', 'y', 'varx', 'varb']

class leastTest(unittest.TestCase):

    def test_discrete(self):
        expr = Transformer('vxr')
        expr.ptsx = [cos(0),2,3,4,5,6]
        expr.ptsy = [x**2 for x in expr.ptsx]
        val = expr.minimize_disc([1, 'vxr'])
        val = val.subs(expr.var,0)
        self.assertTrue(abs(N(val) + 9.333333) < 10**-4)

    def test_discrete_vars(self):
        for varn in [ 'x', 'y', 'van', 'voxfm', 'z', 't', 'w' ]:
            expr = Transformer(varn)
            expr.ptsx = [1,2,3]
            expr.ptsy = [cos(x) for x in expr.ptsx]
            val = expr.minimize_disc([1, varn, varn + '**2'])
            val = val.subs(varn, 0)
            self.assertTrue(abs(N(val) - 1.8793593064) < 10**-4)

    def test_discrete_pot(self):
        for varn in varlist:
            expr = Transformer(varn)
            expr.ptsx = [1,2,3]
            expr.ptsy = [(x**2)+50 for x in expr.ptsx]
            val = expr.minimize_disc_pot()
            val = val.subs(varn, 1)
            self.assertTrue(abs(N(val) - 50.5751542037) < 10**-4)

    def test_discrete_exp(self):
        for varn in varlist:
            expr = Transformer(varn)
            expr.ptsx = [1,2,3]
            expr.ptsy = [x for x in expr.ptsx]
            val = expr.minimize_disc_exp()
            val = val.subs(varn, 1)
            self.assertTrue(abs(N(val) - 1.04911506342) < 10**-4)

    def test_discrete_custom(self):
        expr = Transformer('vxr')
        expr.ptsx = [1,2,3,4,5,6]
        expr.ptsy = [x**2 for x in expr.ptsx]
        val = expr.minimize_disc(['vxr', 'vxr**4', 'sqrt(vxr)', '50*vxr**3'])
        val = val.subs(expr.var,1)
        self.assertTrue(abs(N(val) - 0.967724515512) < 10**-4)

    def test_discrete_pot_err(self):
        for varn in varlist:
            expr = Transformer(varn)
            expr.ptsx = [1,0,3]
            expr.ptsy = [cos(x) for x in expr.ptsx]
            with self.assertRaises(ValueError):
                val = expr.minimize_disc_pot()
                val = val.subs(varn, 1)

    def test_cont(self):
        expr = Transformer('vxr')
        expr.ptsx = [1,2]
        expr.fx = "exp(vxr)"
        val = expr.minimize_cont([1, 'vxr'])
        val = val.subs(expr.var,0)
        self.assertTrue(abs(N(val) + 2.22133020755) < 10**-4)

    def test_cont_custom(self):
        expr = Transformer('vxr')
        expr.ptsx = [1,2]
        expr.fx = "exp(vxr)"
        val = expr.minimize_cont(['vxr', 'vxr**4', 'sqrt(vxr)', '50*vxr**3'])
        val = val.subs(expr.var,1)
        self.assertTrue(abs(N(val) - 2.71615115064) < 10**-4)

    def test_cont_vars(self):
        for varn in [ 'van', 'voxfm' ]:
            expr = Transformer(varn)
            expr.ptsx = [1,2]
            expr.fx = 'cos('+varn+')'
            val = expr.minimize_cont([1, varn])
            val = val.subs(expr.var,0)
            self.assertTrue(abs(N(val) + 2.22133020755) < 10**-4)

    def test_cont_exp(self):
        expr = Transformer('vxr')
        expr.ptsx = [1,2]
        expr.fx = "vxr**2"
        val = expr.minimize_cont_exp()
        val = val.subs(expr.var,1)
        self.assertTrue(abs(N(val) - 1.09456266299) < 10**-4)

    def test_cont_pot(self):
        expr = Transformer('vxr')
        expr.ptsx = [1,2]
        expr.fx = "vxr**2"
        val = expr.minimize_cont_pot()
        val = val.subs(expr.var,2)
        self.assertTrue(abs(N(val) - 4) < 10**-4)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
