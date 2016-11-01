import os
import sys
import unittest

sys.path.append( os.path.join('..', 'leastfun'))
from proc.eparser import *
from proc.least import *

rlist = "cos(0) , 2, 3, 4, 5, 10.123, 33"
wlist = "1 , 2, asd, 4, 5, x, 33"
errlist = "1 , 2, sodf(sdd)++, 4, 5, x, 33"
extreme_case = ",,, ,, ,   ,, ,,"

class parserTest(unittest.TestCase):

    def test_listr_parser(self):
        lval = list_parser( rlist )
        self.assertTrue( lval == [1,2,3,4,5,10.123,33] )

    def test_listw_parser(self):
        lval = list_parser( wlist )
        self.assertTrue( [1,2,sympify("asd"),4,5,sympify("x"),33] == lval )

    def test_extreme_case(self):
        lval = list_parser( extreme_case )
        self.assertFalse( lval )

    def test_error(self):
        lval = list_parser( errlist )
        self.assertFalse( lval )

def main():
    unittest.main()

if __name__ == '__main__':
    main()
