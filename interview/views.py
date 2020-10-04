"""
Overall these views are awful.
- Add back option between steps
- Make use of GeneriViews
- ViewClass
- between each step, post to self, validate data and use next to go to next step
"""
from django.shortcuts import render, redirect

from collections import defaultdict, namedtuple

from .forms import SetupForm, score_form_factory, ObservationsForm, TemplateForm, skip_form_factory
from .models import Template, Question, Score, Interview
from base.models import Candidate, Position, Seniority, Subarea, Area

import uuid, csv, xlrd, io


def setup(request):
    """setup screen render function"""
    form = SetupForm()
    return render(request, 'interview/setup.html', {'form': form})


def evaluation(request):
    """
    Evaluation screen render function.
    Receive data to create interview from query params.
    Store the initial setup data for the interview on the current session.
    """
    candidate_name = request.GET['candidate']
    candidate, _ = Candidate.objects.get_or_create(name=candidate_name)
    request.session['template_id'] = request.GET['template']
    request.session['candidate_id'] = candidate.id
    request.session['position_id'] = request.GET['position']

    template_id = request.GET['template']
    template = Template.objects.get(pk=template_id)
    questions = template.questions.all()

    formatter = lambda q: f'score_{q.id}'
    score_field_names = [formatter(question) for question in questions]
    ScoreForm = score_form_factory(score_field_names)
    score_form = ScoreForm()

    checkbox_formatter = lambda q: f'skip_{q.id}'
    skip_field_names = [checkbox_formatter(question) for question in questions]
    SkipForm = skip_form_factory(skip_field_names)
    skip_form = SkipForm()


    areas = defaultdict(list)
    for question in questions:
        area = question.subarea.area
        areas[area.area].append(question)

    areas = {area: [(i + 1, question, score_form[formatter(question)], skip_form[checkbox_formatter(question)])
                    for i, question in enumerate(questions)]
             for area, questions in areas.items()}

    return render(request, 'interview/evaluation.html', {'areas': areas})


def observations(request):
    store_scores(request)
    return render(request, 'interview/observations.html', {
        'form': ObservationsForm()
    })


def review(request):
    comments = request.POST['comments']
    interviewer_score = request.POST['interviewer_score']
    request.session['comments'] = comments
    request.session['interviewer_score'] = interviewer_score

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
        'interviewer_score': interviewer_score,
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
    interview.interviewer_score = request.session['interviewer_score']
    interview.save()

    question_scores = [(Question.objects.get(pk=pk), score)
                       for pk, score in request.session['scores']]

    for question, score in question_scores:
        Score(question=question, score=score, interview=interview).save()

    return redirect('viz:detail', interview.id)


def template_upload(request):
    if request.POST:
        f = TemplateForm(request.POST, request.FILES)
        f.is_valid()
        template = Template()
        template.name = f.cleaned_data['name']
        template.description = f.cleaned_data['description']
        template.owner = request.user
        uploaded_file = f.cleaned_data['csv']
        file_name = f'/tmp/{str(uuid.uuid4())}.xlsx'
        with open(file_name, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        rows = excel_to_dicts(file_name)
        questions = [add_question_from_template(row) for row in rows]
        template.save()
        template.questions.set(questions)
        template.save()
        return redirect('viz:list')
    else:
        form = TemplateForm()
    return render(request, 'interview/template_upload.html', {
        'form': form
    })


def excel_to_dicts(file):
    book = xlrd.open_workbook(file)
    sheet = book.sheet_by_index(0)
    labels = [cell.value for cell in sheet.row(0)]
    rows = [{label: cell.value for label, cell in zip(labels, row)}
            for row in list(sheet.get_rows())[1:]]
    return rows


def add_question_from_template(row):
    #TODO should be a get as bands are static
    seniority, _ = Seniority.objects.get_or_create(seniority=row['Senioridade'])
    subarea, _ = Subarea.objects.get_or_create(subarea=row['Subarea'])
    area, _ = Area.objects.get_or_create(area=row['Area'])
    if subarea.area != area:
        # TODO assert subarea.area = area, if it isn't throw error
        subarea.area = area
        subarea.save()
    question_body = row['Questao']
    answer = row['Resposta']
    weight = row['Peso']
    question, created = Question.objects.update_or_create(question=question_body, defaults={
        'answer': answer,
        'weight': weight,
        'subarea': subarea,
        'seniority': seniority
    })
    return question

def store_scores(request):
    """
    Store score for each question in session object, does not store score
    for skipped questions
    """
    remove_prefix = lambda key: int(key.split('_')[1])

    skip_pks = [remove_prefix(key) for key, _ in request.POST.items() 
                if 'skip_' in key]

    scores = {remove_prefix(key): int(score) 
              for key, score in request.POST.items() if 'score_' in key}

    request.session['scores'] = [(pk, score) for pk, score in scores.items()
                                 if pk not in skip_pks]
