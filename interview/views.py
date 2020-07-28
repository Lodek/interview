from django.shortcuts import render

from collections import defaultdict, namedtuple

from .forms import SetupForm, score_form_factory, ObservationsForm
from .models import Template, Question, Score, Interview
from base.models import Candidate, Position



def setup(request):
    form = SetupForm()
    return render(request, 'interview/setup.html', {'form': form})


def evaluation(request):
    request.session['template_id'] = request.GET['template']
    request.session['candidate_id'] = request.GET['candidate']
    request.session['position_id'] = request.GET['position']

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


def observations(request):
    extract_pk = lambda key: int(key.replace('score_', ''))
    request.session['scores'] = [(extract_pk(key), int(score))
                                 for key, score in request.POST.items() if 'score_' in key]

    return render(request, 'interview/observations.html', {
        'form': ObservationsForm()
    })


def review(request):
    comments = request.POST['comments']
    request.session['comments'] = comments

    template_id = request.session['template_id'] 
    candidate_id = request.session['candidate_id']
    position_id = request.session['position_id']

    position = Position.objects.get(pk=position_id)
    candidate = Candidate.objects.get(pk=candidate_id)
    template = Template.objects.get(pk=template_id)


    question_scores = [(Question.objects.get(pk=pk), score)
                       for pk, score in request.session['scores']]

    return render(request, 'interview/review.html', {
        'question_scores': question_scores,
        'comments': comments,
        'position': position,
        'candidate': candidate,
        'template': template,
    })


def conclusion(request):
    template_id = request.session['template_id'] 
    candidate_id = request.session['candidate_id']
    position_id = request.session['position_id']

    interview = Interview()
    interview.position = Position.objects.get(pk=position_id)
    interview.candidate = Candidate.objects.get(pk=candidate_id)
    interview.interviewer = request.user
    interview.comments = request.session['comments']
    interview.save()

    question_scores = [(Question.objects.get(pk=pk), score)
                       for pk, score in request.session['scores']]

    for question, score in question_scores:
        Score(question=question, score=score, interview=interview).save()

    return render(request, 'interview/conclusion.html', dict(inteview=interview))
