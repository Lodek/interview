from django.shortcuts import render, get_object_or_404

from interview.models import Interview

from .stats import StatCalculator
from .forms import select_form_factory

import json
import logging

logger = logging.getLogger(__name__)

def detail(request, interview_id):
    interview = get_object_or_404(Interview, pk=interview_id)
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

    interviews = Interview.objects.all()
    form_fields = [f'interview_{interview.id}' for interview in interviews]
    Form = select_form_factory(form_fields)
    form = Form()
    data = [(interview, form[field]) for interview, field in zip(interviews, form_fields)]

    return render(request, 'viz/list.html', {
        'data': data,
    })

def compare(request):
    pks = [int(param.replace('interview_', ''))
           for param in request.GET if 'interview_' in param]
    interviews = Interview.objects.filter(pk__in=pks).all()
    calc = StatCalculator()
    band_per_interview = {interview: calc.calculate_band_avg(interview.question_scores)
                             for interview in interviews}
    area_per_interview = {interview: calc.calculate_area_avg(interview.question_scores)
                             for interview in interviews}
    subarea_per_interview = {interview: calc.calculate_subarea_avg(interview.question_scores)
                             for interview in interviews}
    subarea_data = bucketize(interviews, subarea_per_interview, 'Subarea')
    band_data = bucketize(interviews, band_per_interview, 'Band')
    area_data = bucketize(interviews, area_per_interview, 'Area')
    return render(request, 'viz/compare.html', {
       'subarea_data': json.dumps(subarea_data),
       'area_data': json.dumps(area_data),
       'band_data': json.dumps(band_data),
       'interviews': interviews,
   })

def bucketize(interviews, results_per_interview, header):
    buckets = {bucket for result in results_per_interview.values()
               for bucket in result}
    header = [header] + [interview.candidate.name for interview in interviews]
    body = []
    for bucket in buckets:
        row = [str(bucket)]
        for interview in interviews:
            try:
                row.append(results_per_interview[interview][bucket])
            except KeyError:
                row.append(0)
        body.append(row)
    return [header] + body
