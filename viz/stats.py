"""
module responsible for the interview result calculations
"""
from collections import defaultdict


class StatCalculator:
    """
    Calculate weighted averages for interview groupings
    """

    def calculate_band_avg(self, scores):
        groups = self._grouper(scores, lambda question: question.band)
        return self._calculate_avgs(groups)

    def calculate_subarea_avg(self, scores):
        groups = self._grouper(scores, lambda question: question.subarea)
        return self._calculate_avgs(groups)

    def calculate_area_avg(self, scores):
        groups = self._grouper(scores, lambda question: question.subarea.area)
        return self._calculate_avgs(groups)

    def _grouper(self, scores, group_lambda):
        """Return dictionary of [(question, score)] where questions area grouped by the
        result of group_lambda"""
        groups = defaultdict(list)
        for question, score in scores.items():
            groups[group_lambda(question)].append((question, score))
        return groups

    def _calculate_avgs(self, groups):
        """Calculate the avg for all groups in groups.
        Group is a dict with group as key and list of (question, score) as tuple"""
        return {group: self.calculate_avg(scores) for group, scores in groups.items()}

    def calculate_avg(self, scores):
        """
        Calculate the weighted avg of a list of question and score tuple
        """
        numerator = 0
        denominator = 0
        for question, score in scores:
            numerator += score * question.weight * 2 #2 shifts the scale so score in range(0, 11)
            denominator += question.weight
        return numerator / denominator if denominator else 0
