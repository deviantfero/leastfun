from sympy import *

class Transformer():

    """Class that contains all attributes and methods
       Necessary to apply least squares to a function"""

    def __init__(self, var):
        """
        :var: Symbol to be used

        """
        if(var == 'var'):
            var = 'varn'
        init_printing()
        self.var = symbols(str(var)) 
        self.fx = ""
        self.ptsx = []
        self.ptsy = []
        self.rmat = []
        self.unsolved_m = []
        self.cs = []
        self.eq = 0

    def reset_ans(self):
        """
        Clears the answers from the attributes of a transform object
        """
        self.rmat = []
        self.unsolved_m = []
        self.cs = []
        self.eq = 0


    def minimize_disc(self, aff):
        """Gets the least square polinomial according
        to the aff given

        :aff: the affinity that the aproximate function should have
        :returns: an expression

        """
        self.reset_ans()
        if len(self.ptsx) != len(self.ptsy):
            if len(self.ptsy) == 1:
                tmp = []
                for val in self.ptsx:
                    tmp.append( sympify(self.ptsy[0]).subs(self.var,val) )
                self.oldptsy = tmp
                self.ptsy = tmp
            else:
                raise ValueError('List size invalid')

        for xp in aff:
            self.unsolved_m.append( [ sympify(xp).subs( self.var, pt ) for pt in self.ptsx ] )

        self.unsolved_m = Matrix(self.unsolved_m)

        for i, xp in enumerate(aff):
            tmp = []
            for j, nxp in enumerate(aff):
                m = self.unsolved_m
                tmp.append( m.row(i).dot(m.row(j)) )
            tmp.append( m.row(i).dot( Matrix(self.ptsy)) )
            self.rmat.append(tmp)

        self.rmat = Matrix(self.rmat).rref()[0]

        self.cs = N(self.rmat.col( self.rmat.cols - 1 ))

        for i, el in enumerate(aff):
            self.eq += sympify(el)*round( self.cs[i], 6 )

        return sympify(self.eq)

    def minimize_disc_pot(self):
        """
        Gets the least square with the aff = [1, ln(var)]
        :returns: leastsquare equation where y = exp(leastsquare)
        """
        oldptsy = self.ptsy
        if len(self.ptsy) == 1:
            tmp = []
            for val in self.ptsx:
                tmp.append( log(self.ptsy[0]).subs(self.var,val) )
            self.ptsy = tmp
        else:
            self.ptsy = [log(vary) for vary in self.ptsy]

        for x in self.ptsx:
            if x == 0:
                raise ValueError('No 0 on LN')
        rvalue = exp(self.minimize_disc([1,'ln('+str(self.var)+')']))
        self.ptsy = oldptsy
        return rvalue

    def minimize_disc_exp(self):
        """
        Gets the least square with the aff = [1, var]
        :returns: leastsquare equation where y = exp(leastsquare)
        """
        oldptsy = self.ptsy
        if len(self.ptsy) == 1:
            tmp = []
            for val in self.ptsx:
                tmp.append( log(self.ptsy[0]).subs(self.var,val) )
            self.ptsy = tmp
        else:
            self.ptsy = [log(vary) for vary in self.ptsy]
        rvalue = exp(self.minimize_disc([1, self.var]))
        self.ptsy = oldptsy
        return rvalue

    def minimize_cont(self, aff):
        """Gets the least square polinomial according
        to the aff given, in a continuous range

        :aff: the affinity that the aproximate function should have
        :returns: an expression

        """
        self.reset_ans()
        tmp = []
        if len(self.ptsx) != 2:
            raise ValueError('Wrong range size')

        for xp in aff:
            xp = sympify(xp)
            for yp in aff:
                yp = sympify(yp)
                tmp.append( integrate(sympify(xp)*sympify(yp), (sympify(self.var), self.ptsx[0], self.ptsx[1])) )
            tmp.append( integrate(sympify(xp)*sympify(self.fx), (sympify(self.var), self.ptsx[0], self.ptsx[1])) )
            self.unsolved_m.append(tmp)
            tmp = []

        self.unsolved_m = Matrix(self.unsolved_m)
        self.rmat = Matrix(self.unsolved_m).rref()[0]

        self.cs = N(self.rmat.col( self.rmat.cols - 1 ))

        for i, el in enumerate(aff):
            self.eq += sympify(el)*round( self.cs[i], 6 )

        return sympify(self.eq)

    def minimize_cont_pot(self):
        """
        Gets the least square with the aff = [1, ln(var)]
        in a continuous range
        :returns: leastsquare equation where y = exp(leastsquare)
        """
        self.fx = 'log('+self.fx+')'
        return exp(self.minimize_cont([1, log(self.var)]))

    def minimize_cont_exp(self):
        """
        Gets the least square with the aff = [1, var]
        in a continuous range
        :returns: leastsquare equation where y = exp(leastsquare)
        """
        self.fx = 'log('+self.fx+')'
        return exp(self.minimize_cont([1, self.var]))
