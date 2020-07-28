from django.shortcuts import render

from collections import defaultdict, namedtuple

from .forms import SetupForm, score_form_factory
from .models import Template
from base.models import Candidate, Position

def setup(request):
    form = SetupForm()
    return render(request, 'interview/setup.html', {'form': form})


def evaluation(request):
    request.sessions['template_id'] = request.GET['template']
    request.sessions['candidate_id'] = request.GET['candidate']
    request.sessions['position_id'] = request.GET['position']

    template_id = request.GET['template']
    template = Template.objects.get(pk=template_id)
    questions = template.questions.all()

    formatter = lambda q: f'score_{q.id}'
    field_names = [formatter(question) for question in questions]
    Form = score_form_factory(field_names)
    form = Form()

    areas = defaultdict(list)
    for question in questions:
        area = question.subarea.area
        areas[area.area].append(question)
        
    areas = {area: [(i+1, question, form[formatter(question)])
                    for i, question in enumerate(questions)]
             for area, questions in areas.items()}

    return render(request, 'interview/evaluation.html', {'areas': areas})

def review(request):
    return render(request, 'interview/review.html')
