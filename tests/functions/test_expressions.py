"""
Test the expressions module

:author: Michel Bierlaire
:data: Wed Apr 29 17:47:53 2020

"""
# Bug in pylint
# pylint: disable=no-member
#
# Too constraining
# pylint: disable=invalid-name, too-many-instance-attributes
#
# Not needed in test
# pylint: disable=missing-function-docstring, missing-class-docstring

import unittest
import numpy as np
import biogeme.exceptions as excep
import biogeme.expressions as ex
from biogeme import models
from testData import myData2


class test_expressions(unittest.TestCase):
    def setUp(self):
        self.myData = myData2
        self.Person = ex.Variable('Person')
        self.Variable1 = ex.Variable('Variable1')
        self.Variable2 = ex.Variable('Variable2')
        self.Choice = ex.Variable('Choice')
        self.Av1 = ex.Variable('Av1')
        self.Av2 = ex.Variable('Av2')
        self.Av3 = ex.Variable('Av3')
        self.beta1 = ex.Beta('beta1', 1, None, None, 0)
        self.beta2 = ex.Beta('beta2', 2, None, None, 0)
        self.beta3 = ex.Beta('beta3', 3, None, None, 1)
        self.beta4 = ex.Beta('beta4', 2, None, None, 1)
        self.omega1 = ex.RandomVariable('omega1')
        self.omega2 = ex.RandomVariable('omega2')
        self.xi1 = ex.bioDraws('xi1', 'NORMAL')
        self.xi2 = ex.bioDraws('xi2', 'UNIF')
        self.xi3 = ex.bioDraws('xi3', 'WRONGTYPE')

    def test_isNumeric(self):
        result = ex.isNumeric(1)
        self.assertTrue(result)
        result = ex.isNumeric(0.1)
        self.assertTrue(result)
        result = ex.isNumeric(True)
        self.assertTrue(result)
        result = ex.isNumeric(self)
        self.assertFalse(result)

    def test_add(self):
        result = self.Variable1 + self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 + Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 + 1
        self.assertEqual(result.__str__(), '(Variable1 + `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 + self.Variable1
        self.assertEqual(result.__str__(), '(`1` + Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self + self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 + self

    def test_sub(self):
        result = self.Variable1 - self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 - Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 - 1
        self.assertEqual(result.__str__(), '(Variable1 - `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 - self.Variable1
        self.assertEqual(result.__str__(), '(`1` - Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self - self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 - self

    def test_mul(self):
        result = self.Variable1 * self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 * Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 * 1
        self.assertEqual(result.__str__(), '(Variable1 * `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 * self.Variable1
        self.assertEqual(result.__str__(), '(`1` * Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self * self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 * self

    def test_div(self):
        result = self.Variable1 / self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 / Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 / 1
        self.assertEqual(result.__str__(), '(Variable1 / `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 / self.Variable1
        self.assertEqual(result.__str__(), '(`1` / Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self / self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 / self

    def test_neg(self):
        result = -self.Variable1
        self.assertEqual(result.__str__(), '(-Variable1)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

    def test_pow(self):
        result = self.Variable1 ** self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 ** Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 ** 1
        self.assertEqual(result.__str__(), '(Variable1 ** `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 ** self.Variable1
        self.assertEqual(result.__str__(), '(`1` ** Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self ** self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 ** self

    def test_and(self):
        result = self.Variable1 & self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 and Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 & 1
        self.assertEqual(result.__str__(), '(Variable1 and `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 & self.Variable1
        self.assertEqual(result.__str__(), '(`1` and Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self & self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 & self

    def test_or(self):
        result = self.Variable1 | self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 or Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 | 1
        self.assertEqual(result.__str__(), '(Variable1 or `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 | self.Variable1
        self.assertEqual(result.__str__(), '(`1` or Variable1)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self | self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 | self

    def test_eq(self):
        result = self.Variable1 == self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 == Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 == 1
        self.assertEqual(result.__str__(), '(Variable1 == `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 == self.Variable1
        self.assertEqual(result.__str__(), '(Variable1 == `1`)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self == self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 == self

    def test_neq(self):
        result = self.Variable1 != self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 != Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 != 1
        self.assertEqual(result.__str__(), '(Variable1 != `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 != self.Variable1
        self.assertEqual(result.__str__(), '(Variable1 != `1`)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self != self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 != self

    def test_le(self):
        result = self.Variable1 <= self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 <= Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 <= 1
        self.assertEqual(result.__str__(), '(Variable1 <= `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 <= self.Variable1
        self.assertEqual(result.__str__(), '(Variable1 >= `1`)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self <= self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 <= self

    def test_ge(self):
        result = self.Variable1 >= self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 >= Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 >= 1
        self.assertEqual(result.__str__(), '(Variable1 >= `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 >= self.Variable1
        self.assertEqual(result.__str__(), '(Variable1 <= `1`)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self >= self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 >= self

    def test_lt(self):
        result = self.Variable1 < self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 < Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 < 1
        self.assertEqual(result.__str__(), '(Variable1 < `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 < self.Variable1
        self.assertEqual(result.__str__(), '(Variable1 > `1`)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self < self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 < self

    def test_gt(self):
        result = self.Variable1 > self.Variable2
        self.assertEqual(result.__str__(), '(Variable1 > Variable2)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(result.children[1]) is self.Variable2
        self.assertTrue(self.Variable1.parent is result)
        self.assertTrue(self.Variable2.parent is result)

        result = self.Variable1 > 1
        self.assertEqual(result.__str__(), '(Variable1 > `1`)')
        self.assertTrue(result.children[0]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        result = 1 > self.Variable1
        self.assertEqual(result.__str__(), '(Variable1 < `1`)')
        self.assertTrue(result.children[1]) is self.Variable1
        self.assertTrue(self.Variable1.parent is result)

        with self.assertRaises(excep.biogemeError):
            result = self > self.Variable1

        with self.assertRaises(excep.biogemeError):
            result = self.Variable1 > self

    def test_getValue_c(self):
        result = self.Variable1.getValue_c(self.myData)
        np.testing.assert_equal(result, [10, 20, 30, 40, 50])

    def test_DefineVariable(self):
        _ = ex.DefineVariable(
            'newvar', self.Variable1 + self.Variable2, self.myData
        )
        cols = self.myData.data.columns
        added = 'newvar' in cols
        self.assertTrue(added)

    def test_expr1(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        self.assertAlmostEqual(expr1.getValue(), 1.954888238921129, 5)
        res = expr1.getValue_c(self.myData)
        for v in res:
            self.assertAlmostEqual(v, 1.954888238921129, 5)

    def test_setOfBetas(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        s = expr1.setOfBetas()
        self.assertSetEqual(s, {'beta1', 'beta2'})
        s = expr1.setOfBetas(free=False, fixed=True)
        self.assertSetEqual(s, {'beta3'})
        s = expr1.setOfBetas(free=True, fixed=True)
        self.assertSetEqual(s, {'beta1', 'beta2', 'beta3'})

    def test_setOfVariables(self):
        expr1 = 2 * self.Variable1 - ex.exp(-self.Variable2) / (
            self.Variable1 * (self.Variable1 >= self.Variable2)
        )
        s = expr1.setOfVariables()
        self.assertSetEqual(s, {'Variable1', 'Variable2'})

    def test_getElementaryExpression(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        ell = expr1.getElementaryExpression('beta2')
        self.assertEqual(ell.name, 'beta2')

    def test_expr2(self):
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        res = list(expr2.getValue_c(self.myData))
        self.assertListEqual(res, [20.0, 40.0, 60.0, 80.0, 100.0])

    def test_dictOfBetas(self):
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        b = expr2.dictOfBetas(free=True, fixed=True)
        # Note that the following checks only the labels. Its probably
        # good enough for our purpose.
        self.assertDictEqual(
            b, {'beta1': 0, 'beta2': self.beta2, 'beta3': self.beta3}
        )

    def test_dictOfVariables(self):
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        b = expr2.dictOfVariables()
        # Note that the following checks only the labels. Its probably
        # good enough for our purpose.
        self.assertDictEqual(
            b, {'Variable1': self.Variable1, 'Variable2': self.Variable2}
        )

    def test_dictOfRandomVariables(self):
        expr = -(self.omega1 + self.omega2 + self.Variable1)
        b = expr.dictOfRandomVariables()
        self.assertDictEqual(b, {'omega1': self.omega1, 'omega2': self.omega2})

    def test_dictOfDraws(self):
        expr = -(self.xi1 + self.xi2 - self.xi3 + self.Variable1)
        b = expr.dictOfDraws()
        self.assertDictEqual(
            b, {'xi1': 'NORMAL', 'xi2': 'UNIF', 'xi3': 'WRONGTYPE'}
        )

    def test_setRow(self):
        expr = self.Variable1 + self.Variable2
        df = self.myData.data
        row_0 = df.iloc[0]
        expr.setRow(row_0)
        self.assertEqual(expr.getValue(), 110)
        row_1 = df.iloc[1]
        expr.setRow(row_1)
        self.assertEqual(expr.getValue(), 220)
        expr.setRow(1)
        with self.assertRaises(excep.biogemeError):
            expr.getValue()

    def test_setUniqueId(self):
        expr1 = self.beta1
        ids = {'beta1': 0}
        expr1.setUniqueId(ids)
        self.assertEqual(expr1.uniqueId, 0)

        expr2 = (
            2 * self.beta1 * self.Variable1
            - ex.exp(-self.beta2 * self.Variable2)
            / (self.beta3 * (self.beta2 >= self.beta1))
            - self.omega1
            + self.xi3
        )
        ids = {
            'beta1': 0,
            'beta2': 1,
            'beta3': 2,
            'omega1': 3,
            'xi3': 4,
            'Variable1': 5,
            'Variable2': 6,
        }
        expr2.setUniqueId(ids)
        self.assertEqual(self.beta1.uniqueId, 0)
        self.assertEqual(self.beta2.uniqueId, 1)
        self.assertEqual(self.beta3.uniqueId, 2)
        self.assertEqual(self.omega1.uniqueId, 3)
        self.assertEqual(self.xi3.uniqueId, 4)
        self.assertEqual(self.Variable1.uniqueId, 5)
        self.assertEqual(self.Variable2.uniqueId, 6)

        expr3 = self.xi2
        ids = {'anything': 0}
        with self.assertRaises(excep.biogemeError):
            expr3.setUniqueId(ids)
        
        ids = {'xi2': 'error'}
        with self.assertRaises(excep.biogemeError):
            expr3.setUniqueId(ids)
        
    def test_setSpecificIndices(self):
        expr1 = self.beta1
        expr1.setSpecificIndices(
            {'beta1': 12},
            None,
            None,
            None,
        )
        self.assertEqual(expr1.betaId, 12)
        with self.assertRaises(excep.biogemeError):
            expr1.setSpecificIndices(
                None,
                {'beta1': 12},
                None,
                None,
            )
        self.beta3.setSpecificIndices(
                None,
                {'beta3': 13},
                None,
                None,
        )
        self.assertEqual(self.beta3.betaId, 13)
        with self.assertRaises(excep.biogemeError):
            self.beta3.setSpecificIndices(
                None,
                {'beta1': 13},
                None,
                None,
            )
        with self.assertRaises(excep.biogemeError):
            self.beta3.setSpecificIndices(
                {'beta3': 13},
                None,
                None,
                None,
            )
        self.omega1.setSpecificIndices(
                None,
                None,
                {'omega1': 14},
                None,
        )
        self.assertEqual(self.omega1.rvId, 14)
        with self.assertRaises(excep.biogemeError):
            self.omega1.setSpecificIndices(
                None,
                None,
                {'omega3': 14},
                None,
            )
        with self.assertRaises(excep.biogemeError):
            self.omega1.setSpecificIndices(
                None,
                {'omega1': 14},
                None,
                None,
            )
        self.xi1.setSpecificIndices(
                None,
                None,
                None,
                {'xi1': 15},
        )
        self.assertEqual(self.xi1.drawId, 15)
        with self.assertRaises(excep.biogemeError):
            self.xi1.setSpecificIndices(
                None,
                None,
                None,
                {'xi2': 15},
            )
        with self.assertRaises(excep.biogemeError):
            self.xi1.setSpecificIndices(
                None,
                None,
                {'xi1': 15},
                None,
            )

        expr2 = (
            2 * self.beta1 * self.Variable1
            - ex.exp(-self.beta2 * self.Variable2)
            / (self.beta3 * (self.beta2 >= self.beta1))
            - self.omega1
            + self.xi3
        )

        expr2.setSpecificIndices(
            {'beta1':0, 'beta2': 1},
            {'beta3':0, 'beta4': 1},
            {'omega1':0, 'omega2': 1},
            {'xi1': 0, 'xi2': 1, 'xi3': 2},
            )
        self.assertEqual(self.beta1.betaId, 0)
        self.assertEqual(self.beta2.betaId, 1)
        self.assertEqual(self.beta3.betaId, 0)
        self.assertEqual(self.omega1.rvId, 0)
        self.assertEqual(self.xi3.drawId, 2)

        
        return

    
        
        
    def test_getClassName(self):
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        c = expr2.getClassName()
        self.assertEqual(c, 'Minus')

    def test_signature(self):
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        expr2._prepareFormulaForEvaluation(self.myData)
        s = expr2.getSignature()
        self.assertEqual(len(s), 17)

    def test_expr3(self):
        myDraws = ex.bioDraws('myDraws', 'UNIFORM')
        expr3 = ex.MonteCarlo(myDraws * myDraws)
        res = expr3.getValue_c(self.myData, numberOfDraws=100000)
        for v in res:
            self.assertAlmostEqual(v, 1.0 / 3.0, 2)

    def test_expr4(self):
        omega = ex.RandomVariable('omega')
        a = 0
        b = 1
        x = a + (b - a) / (1 + ex.exp(-omega))
        dx = (b - a) * ex.exp(-omega) * (1 + ex.exp(-omega)) ** (-2)
        integrand = x * x
        expr4 = ex.Integrate(integrand * dx / (b - a), 'omega')
        res = expr4.getValue_c(self.myData)
        for v in res:
            self.assertAlmostEqual(v, 1.0 / 3.0, 2)

    def test_expr5(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        expr5 = ex.Elem({1: expr1, 2: expr2}, self.Person) / 10
        res = list(expr5.getValue_c(self.myData))
        self.assertListEqual(
            res,
            [
                0.19548882389211292,
                0.19548882389211292,
                0.19548882389211292,
                8.0,
                10.0,
            ],
        )

    def test_expr6(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        omega = ex.RandomVariable('omega')
        a = 0
        b = 1
        x = a + (b - a) / (1 + ex.exp(-omega))
        dx = (b - a) * ex.exp(-omega) * (1 + ex.exp(-omega)) ** (-2)
        integrand = x * x
        expr4 = ex.Integrate(integrand * dx / (b - a), 'omega')
        expr6 = ex.bioMultSum([expr1, expr2, expr4])
        res = list(expr6.getValue_c(self.myData))
        self.assertListEqual(
            res,
            [
                22.28822055098741,
                42.28822055098741,
                62.28822055098741,
                82.2882205509874,
                102.2882205509874,
            ],
        )

    def test_expr7(self):
        V = {0: -self.beta1, 1: -self.beta2, 2: -self.beta1}
        av = {0: 1, 1: 1, 2: 1}
        expr7 = ex.LogLogit(V, av, 1)
        r = expr7.getValue()
        self.assertAlmostEqual(r, -1.861994804058251, 5)
        expr8 = models.loglogit(V, av, 1)
        res = expr8.getValue_c(self.myData)
        for v in res:
            self.assertAlmostEqual(v, -1.861994804058251, 5)

    def test_expr9(self):
        V = {0: -self.beta1, 1: -self.beta2, 2: -self.beta1}
        av = {0: 1, 1: 1, 2: 1}
        expr8 = models.loglogit(V, av, 1)
        expr9 = ex.Derive(expr8, 'beta2')
        res = expr9.getValue_c(self.myData)
        for v in res:
            self.assertAlmostEqual(v, -0.8446375965030364, 5)

    def test_expr10(self):
        expr10 = ex.bioNormalCdf(self.Variable1 / 10 - 1)
        res = expr10.getValue_c(self.myData)
        for i, j in zip(
            res,
            [
                0.5,
                0.8413447460685283,
                0.9772498680518218,
                0.99865010196837,
                0.9999683287581669,
            ],
        ):
            self.assertAlmostEqual(i, j, 5)

    def test_expr11(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        expr5 = ex.Elem({1: expr1, 2: expr2}, self.Person) / 10
        expr10 = ex.bioNormalCdf(self.Variable1 / 10 - 1)
        expr11 = ex.bioMin(expr5, expr10)
        res = expr11.getValue_c(self.myData)
        for i, j in zip(
            res,
            [
                0.19548882389211292,
                0.19548882389211292,
                0.19548882389211292,
                0.99865010196837,
                0.9999683287581669,
            ],
        ):
            self.assertAlmostEqual(i, j, 5)

    def test_expr12(self):
        expr1 = 2 * self.beta1 - ex.exp(-self.beta2) / (
            self.beta3 * (self.beta2 >= self.beta1)
        )
        expr2 = 2 * self.beta1 * self.Variable1 - ex.exp(
            -self.beta2 * self.Variable2
        ) / (self.beta3 * (self.beta2 >= self.beta1))
        expr5 = ex.Elem({1: expr1, 2: expr2}, self.Person) / 10
        expr10 = ex.bioNormalCdf(self.Variable1 / 10 - 1)
        expr12 = ex.bioMax(expr5, expr10)
        res = expr12.getValue_c(self.myData)
        for i, j in zip(
            res, [0.5, 0.8413447460685283, 0.9772498680518218, 8.0, 10.0]
        ):
            self.assertAlmostEqual(i, j, 5)


if __name__ == '__main__':
    unittest.main()