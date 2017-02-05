import sympy
from sympy.parsing.sympy_parser import parse_expr
import itertools as it
import math

class Sequence(object):
    '''A sequence object'''

    def __init__(self, sequence='1, 3, 5, 7, 217341'):
        try:
            self._seq = [float(i) for i in sequence.replace(' ','').split(',')]
        except ValueError:
            raise ValueError('invalid numbers')
        self._seqLen = len(self._seq)

    def _isArithmetic(self):
        '''When A_n = pn + q'''
        if len(self._seq) <= 2:
            if len(self._seq) == 1:
                return False, None
            elif len(self._seq) == 2:
                return True, self._seq[1] - self._seq[0]
        d = self._seq[1] - self._seq[0]
        if all([self._seq[i+1]-self._seq[i]==d for i in range(1, len(self._seq)-1)]):
            return True, d
        return False, None

    def _isGeometric(self):
        '''When A_n = p^(n-1) * q, or in special cases, A_n = p^(n+q)'''
        if len(self._seq) <= 2:
            if len(self._seq) == 1:
                return False, None
            elif len(self._seq) == 2:
                return True, self._seq[1] / self._seq[0]
        r = self._seq[1] / self._seq[0]
        if all([self._seq[i+1]/self._seq[i]==r for i in range(1, len(self._seq)-1)]):
            return True, r
        return False, None

    def generateFormula(self):
        '''Generates a formula for the sequence, returns a sympy object.\nMay not work for complex sequences.'''
        arithmetic, d = self._isArithmetic()
        if arithmetic:
            self.formula = sympy.nsimplify(parse_expr('{}*n + {}'.format(d, self._seq[0]-d)))
            return self.formula
        geometric, r = self._isGeometric()
        if geometric:
            log = math.log(self._seq[0], r)
            if log.is_integer():
                self.formula = sympy.nsimplify(parse_expr('{}**(n-1+{})'.format(r, log)))
            else:
                self.formula = sympy.nsimplify(parse_expr('{}**(n-1) * {}'.format(r, self._seq[0])))
            return self.formula
        else:
            tmp = []
            combinations = [i for i in it.combinations([l+1 for l in range(self._seqLen)], self._seqLen-1)]
            for combination, leftOut in zip(combinations, reversed([l+1 for l in range(self._seqLen)])):
                numerator = sympy.expand(parse_expr('*'.join(['(n-{})'.format(element) for element in combination])))
                denominator = parse_expr('*'.join(['({}-{})'.format(leftOut,element) for element in combination]))
                tmp.append(numerator / denominator)
            fractions = []
            for sequenceItem, element in zip(reversed(self._seq), tmp):
                fractions.append(sympy.nsimplify(sequenceItem) * element)
            self.formula = sympy.expand(sum(fractions))
            return self.formula
