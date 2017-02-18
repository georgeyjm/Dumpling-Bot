import sympy
from sympy.parsing.sympy_parser import parse_expr
import itertools as it
import math
from random import choice, random
from math import sqrt, degrees, radians, pi

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

class trig:

    allVals = {'sin':{0:0, 15:(sqrt(6)-sqrt(2))/4, 30:1/2, 45:sqrt(2)/2, 60:sqrt(3)/2, 75:(sqrt(6)+sqrt(2))/4, 90:1},
               'tan':{0:0, 15:2-sqrt(3), 30:sqrt(3)/3, 45:1, 60:sqrt(3), 75:2+sqrt(3)}}
    unifyFunc = {'sin':'sin','cos':'sin','tan':'tan','cot':'tan'}
    switchFunc = {'sin':'cos','tan':'cot'}

    def trig_val(func, param, mode='degrees'):
        if not (mode in trig.MODES and func in ('sin','cos','tan','cot') and (isinstance(param, int) or isinstance(param, float))):
            raise ValueError('invalid parameters')
        if mode == 'radians':
            param = round(param*(180/pi)) # 弧度转角度
        if func in ('cos','cot'):
            param = 90 - param
        func = trig.unifyFunc[func] # 互余角三角函数的关系 (排除余弦余切，方便后面判断)
        param -= param - param%360 # 终边相等，函数值不变。将角度限制在360度之内，同时排除负角度情况
        if param > 90:
            sign = 1
            multiple = param - param%90
            if (func == 'sin' and param > 180) or (func == 'tan' and (param < 180 or param > 270)):
                sign = -1 # 符号看象限
            if multiple//90 % 2 == 1: # 奇变偶不变
                return sign * trig.trig_val(trig.switchFunc[func], param - multiple)
            return sign * trig.trig_val(func, param - multiple)
        try:
            return trig.allVals[func][param] # 第一象限角
        except KeyError:
            raise ValueError('only accept special angle values') # 非特殊角

    def parseAnswer(decimal):
        val = '{:.5f}'.format(decimal)
        sign = ''
        if decimal < 0:
            sign = '-'
            val = val[1:]
        if val == '0.00000':
            return '0'
        elif val == '1.00000':
            return '{}1'.format(sign)
        elif val == '0.50000':
            return '{}1/2 = {}0.5'.format(sign,sign)
        elif val == '0.70711':
            return '{}√2/2 ≈ {}0.707'.format(sign,sign)
        elif val == '0.86603':
            return '{}√3/2 ≈ {}0.866'.format(sign,sign)
        elif val == '0.57735':
            return '{}√3/3 ≈ {}0.577'.format(sign,sign)
        elif val == '1.73205':
            return '{}√3 ≈ {}1.732'.format(sign,sign)
        elif val == '0.25882':
            return '{}(√6-√2)/4 ≈ {}0.259'.format(sign,sign)
        elif val == '0.96593':
            return '{}(√6+√2)/4 ≈ {}0.966'.format(sign,sign)
        elif val == '0.26795':
            if sign == '-':
                return '-2+√3 ≈ -0.268'
            else:
                return '2-√3 ≈ 0.268'
        elif val == '3.73205':
            if sign == '-':
                return '-2-√3 ≈ -3.732'
            else:
                return '2+√3 ≈ 3.732'
        raise ValueError('invalid value to parse')

    # DIFFICULTY = 1 # 1=Easy, 2=Hard
    MODES = ('degrees', 'radians')
    # if DIFFICULTY == 1:
    #     specials = (0,30,45,60,90)
    #     specialRads = ([0,1],[1,6],[1,4],[1,3],[1,2],[2,3],[5,6])
    #     FUNCTIONS = ('sin', 'cos', 'tan')
    #     possibility = {0:20, 1:15, 2:15, 3:10, 4:10, 5:5}
    #     radP = {0:20, 1:15, 2:10}
    #     negP = 0.3
    # elif DIFFICULTY == 2:
    #     specials = (0,15,30,45,60,75,90)
    #     specialRads = ([0,1],[1,12],[1,6],[1,4],[1,3],[5,12],[1,2],[7,12],[2,3],[3,4],[5,6],[11,12])
    #     FUNCTIONS = ('sin', 'cos', 'tan', 'cot')
    #     possibility = {0:1, 1:1, 2:1, 3:1, 4:1, 5:1}
    #     radP = {0:1, 1:1, 2:1, 3:1}
    #     negP = 0.5
    # addon = [i for i,j in possibility.items() for k in range(j)]
    # radAddon = [i for i,j in radP.items() for k in range(j)]

    # while True:
    #     mode = choice(MODES)
    #     if mode == 'degrees':
    #         question = choice(specials) + choice(addon) * 90
    #         if random() < negP:
    #             question = -question
    #         while True:
    #             function = choice(FUNCTIONS)
    #             if (function == 'tan' and question % 90 == 0 and question // 90 % 2 == 1) or \
    #                (function == 'cot' and question % 180 == 0):
    #                 continue
    #             break
    #         while True:
    #             answer = input('{}({}°) = '.format(function, question))
    #             if function not in answer and 'trig_val' not in answer:
    #                 try:
    #                     answerVal = eval(answer)
    #                 except Exception:
    #                     print('Invalid input!\n')
    #                     continue
    #                 correct = trig_val(function, question)
    #                 if answerVal == correct:
    #                     print('Correct!\n')
    #                     break
    #                 else:
    #                     print('Incorrect!\nThe answer is {}\n'.format(parseAnswer(correct)))
    #                     break
    #             else:
    #                 print('Cheater!\n')
    #     elif mode == 'radians':
    #         qNum, qDen = choice(specialRads)
    #         qNum += choice(radAddon) * qDen
    #         if random() < negP:
    #             qNum = -qNum
    #         while True:
    #             function = choice(FUNCTIONS)
    #             if (function == 'tan' and qDen == 2 and qNum % 2 == 1) or \
    #                (function == 'cot' and qDen == 1):
    #                 continue
    #             break
    #         while True:
    #             numer = '{}π'.format(qNum)
    #             denom = '/{}'.format(qDen)
    #             if abs(qNum) == 1:
    #                 if qNum == -1:
    #                     numer = '-π'
    #                 else:
    #                     numer = 'π'
    #             if qDen == 1:
    #                 denom = ''
    #             if qNum == 0:
    #                 numer = '0'
    #                 denom = ''
    #             answer = input('{}({}{}) = '.format(function, numer, denom))
    #             if function not in answer and 'trig_val' not in answer:
    #                 try:
    #                     answerVal = eval(answer)
    #                 except Exception:
    #                     print('Invalid input!\n')
    #                     continue
    #                 correct = trig_val(function, qNum*pi/qDen, 'radians')
    #                 if answerVal == correct:
    #                     print('Correct!\n')
    #                     break
    #                 else:
    #                     print('Incorrect!\nThe answer is {}\n'.format(parseAnswer(correct)))
    #                     break
    #             else:
    #                 print('Cheater!\n')
