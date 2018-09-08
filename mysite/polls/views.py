
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# Create your views here.
import json
from .models import Question, Choice


def index(request):
    return HttpResponse("hello World")


def foo(request):
    return HttpResponse("Hello Foo")


def get_all_question(request):
    question_list = [q.to_dict() for q in Question.objects.all()]
    item = {"items": question_list}
    json_data = json.dumps(item, indent=4)
    return HttpResponse(json_data, content_type='application/json')


def get_question(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    question = question.to_dict()
    json_data = json.dumps(question, indent=4)
    return HttpResponse(json_data, content_type="application/json")


def display_all_question(request):
    question = Question.objects.all()
    choice = Choice.objects.all()
    context = {'question': question, 'choice': choice}
    return render(request, 'polls/Questions.html', context)


def question_votes(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        return render(request, 'polls/question_votes.html', {'question': question})
    elif request.method == 'POST':
        vote_key = "question {}".format(question.id)
        check_session = request.session.get(vote_key)
        if check_session is None:
            choice_id = int(request.POST['choice'])
            request.session[vote_key] = question_id
            choice = Choice.objects.get(pk=choice_id)
            choice.votes += 1
            choice.save()
            request.session.save()
            return HttpResponseRedirect("/polls/questions")
        else:
            return HttpResponse("You can't vote")
