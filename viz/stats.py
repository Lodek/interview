"""
module responsible for the interview result calculations
"""
from collections import defaultdict


class StatCalculator:
    """
    Calculate weighted averages for interview groupings
    """
    def __init__(self, scores):
        self.scores = scores

    def calculate_band_avg(self):
        groups = self._grouper(lambda question: question.band)
        return self._calculate_avg(groups)

    def calculate_subarea_avg(self):
        groups = self._grouper(lambda question: question.band.subarea)
        return self._calculate_avg(groups)

    def calculate_area_avg(self):
        groups = self._grouper(lambda question: question.area)
        return self._calculate_avg(groups)

    def _grouper(self, group_lambda):
        """Return dictionary of [(question, score)] where questions area grouped by the
        result of group_lambda"""
        groups = defaultdict(list)
        for question, score in self.scores.items():
            groups[group_lambda(question)].append((question, score))
        return groups

    def _calculate_avg(self, groups):
        """Return dictionary of the weighted average for grouped scores.
        Keys in the dictionary are the same as groups dict"""
        zero_factory = lambda: 0
        numerator = defaultdict(zero_factory)
        denominator = defaultdict(zero_factory)
        for group, scores in groups:
            for question, score in scores:
                numerator[group] += score * question.weight
                denominator[group] += question.weight
        results = {}
        for group in numerator:
            results[group] = numerator[group] / denominator[group]
        return results
