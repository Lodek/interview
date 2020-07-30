from django.shortcuts import render

from interview.models import Interview

from .stats import StatCalculator

import json

def detail(request, interview_id):
    interview = Interview.objects.get(pk=interview_id)
    question_scores = interview.question_scores
    calculator = StatCalculator()
    area_results = [[area.area, result]
                    for area, result in calculator.calculate_area_avg(question_scores).items()]
    band_results = [[band.band, result]
                    for band, result in calculator.calculate_band_avg(question_scores).items()]
    subarea_results = [[subarea.subarea, result]
                       for subarea, result in calculator.calculate_subarea_avg(question_scores).items()]
    
    return render(request, 'viz/detail.html', {
        'interview': interview,
        'area_results': json.dumps(area_results),
        'band_results': json.dumps(band_results),
        'subarea_results': json.dumps(subarea_results),
    })

def list(request):

    return render(request, 'viz/list.html', {
        'interviews': Interview.objects.all()
    })
