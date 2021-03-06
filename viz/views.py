from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from interview.models import Interview

from .stats import StatCalculator
from .forms import select_form_factory, ListFilterForm

import json
import logging

logger = logging.getLogger(__name__)

def detail(request, interview_id):
    interview = get_object_or_404(Interview, pk=interview_id)
    question_scores = interview.question_scores
    calculator = StatCalculator()
    area_results = [[area.area, result]
                    for area, result in calculator.calculate_area_avg(question_scores).items()]
    seniority_results = [[seniority.seniority, result]
                    for seniority, result in calculator.calculate_seniority_avg(question_scores).items()]
    subarea_results = [[subarea.subarea, result]
                       for subarea, result in calculator.calculate_subarea_avg(question_scores).items()]
    
    return render(request, 'viz/detail.html', {
        'interview': interview,
        'area_results': json.dumps(area_results),
        'seniority_results': json.dumps(seniority_results),
        'subarea_results': json.dumps(subarea_results),
    })

def filter_factory(param, value):
    if param == 'from_date':
        return {'date__gte': value}
    if param == 'to_date':
        return {'date__lte': value}
    if param == 'candidate':
        return {'candidate__name__regex': f'.*{value.lower()}.*'}
    else:
        return {}

def list(request):
    queryset = Interview.objects
    for key, value in request.GET.items():
        if value:
            filter = filter_factory(key, value)
            if filter:
                queryset = queryset.filter(**filter)
    interviews = queryset.all()
    form_fields = [f'interview_{interview.id}' for interview in interviews]
    Form = select_form_factory(form_fields)
    form = Form()
    data = [(interview, form[field]) for interview, field in zip(interviews, form_fields)]

    filter_init = {'candidate': request.GET.get('candidate', '')}
    filter_form = ListFilterForm(initial=filter_init)

    return render(request, 'viz/list.html', {
        'data': data,
        'filter_form': filter_form
    })

def compare(request):
    pks = [int(param.replace('interview_', ''))
           for param in request.GET if 'interview_' in param]
    interviews = Interview.objects.filter(pk__in=pks).all()
    calc = StatCalculator()
    seniority_per_interview = {interview: calc.calculate_seniority_avg(interview.question_scores)
                             for interview in interviews}
    area_per_interview = {interview: calc.calculate_area_avg(interview.question_scores)
                             for interview in interviews}
    subarea_per_interview = {interview: calc.calculate_subarea_avg(interview.question_scores)
                             for interview in interviews}
    subarea_data = bucketize(interviews, subarea_per_interview, 'Subarea')
    seniority_data = bucketize(interviews, seniority_per_interview, 'Seniority')
    area_data = bucketize(interviews, area_per_interview, 'Area')
    return render(request, 'viz/compare.html', {
       'subarea_data': json.dumps(subarea_data),
       'area_data': json.dumps(area_data),
       'seniority_data': json.dumps(seniority_data),
       'interviews': interviews,
   })


def json_export(request, interview_id):
    interview = get_object_or_404(Interview, pk=interview_id)
    json = interview.jsonfy()
    return HttpResponse(json)

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
