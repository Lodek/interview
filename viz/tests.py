from django.test import TestCase

from interview.models import Question

from .stats import StatCalculator


class StatCalculatorTest(TestCase):

    def setUp(self):
        self.calc = StatCalculator()
        self.scores = [
            (Question(weight=3), 3),
            (Question(weight=2), 1),
        ]

    def test_calculate_avg(self):
        avg = self.calc.calculate_avg(self.scores)
        self.assertEqual(avg, 11/5)
        
    def test_calculate_avgs(self):
        groups = {
            'a': self.scores,
            'b': self.scores,
        }
        avgs = self.calc._calculate_avgs(groups)
        self.assertEqual(avgs['a'], 11/5)
        self.assertEqual(avgs['b'], 11/5)
