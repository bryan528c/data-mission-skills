"""Independently computed fictional examples; NOT end-to-end skill evals."""
from fractions import Fraction
from math import hypot
import unittest

class ExampleChecks(unittest.TestCase):
    def test_market_weighted_margin(self):
        self.assertEqual(Fraction(10+180,100+900),Fraction(19,100))
        self.assertNotEqual(Fraction(10,100)/2+Fraction(180,900)/2,Fraction(19,100))
    def test_supplier_missing_test_not_pass(self):
        evidence=None
        state='unverified' if evidence is None else ('pass' if evidence else 'fail')
        self.assertEqual(state,'unverified')
    def test_transport_single_trip_lower_bound(self):
        capacity=[40,40];demand=85
        self.assertEqual(max(0,demand-sum(capacity)),5)
    def test_meal_response_denominator(self):
        self.assertEqual(Fraction(15,20),Fraction(3,4))
        self.assertNotEqual(Fraction(15,100),Fraction(3,4))
    def test_camera_union(self):
        a={1,2,3};b={3,4}
        self.assertEqual(len(a|b),4)
        self.assertNotEqual(len(a)+len(b),len(a|b))
    def test_overlay_axis_and_norm_differ(self):
        x=y=4;limit=5
        self.assertTrue(abs(x)<=limit and abs(y)<=limit)
        self.assertGreater(hypot(x,y),limit)
        self.assertEqual((-6+6)/2,0)
    def test_value_chain_relation_not_coefficient(self):
        edges=[{'from':'A','to':'B','type':'supplies'},{'from':'B','to':'C','type':'supplies'}]
        self.assertTrue(all('coefficient' not in e for e in edges))
    def test_education_objective_and_assessment_distinct(self):
        goal='explain_relationship'
        evidence={'recall_acronyms'}
        self.assertNotIn(goal,evidence)

if __name__=='__main__':unittest.main()
