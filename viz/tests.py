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

class ComparationTest(TestCase):
    
    def test_compare(self):

        john = 'John'
        steve = 'Steve'


        johns_iterview = Interview(candidate=john)
        steves_iterview = Interview(candidate=steve)


        band_standings = {
            'B1': {
                'John': 8,
                'Steve': 9
            },
            'B2': {
                'John': 4,
                'Steve': 8
            },
            'B3': {
                'John': 2,
                'Steve': 9
            }
        }
