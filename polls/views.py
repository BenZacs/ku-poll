import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Question, Choice, Vote
from django.template import loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def index(request):
    """Create the index page."""
    latest_question_list = Question.objects.order_by('-pub_date')[:]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list, }
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    """Create the result page."""
    question = get_object_or_404(Question, pk=question_id)
    user_exist = Vote.objects.filter(pk=question_id, user_id=request.user.id).exists()
    return render(request, 'polls/results.html', {'question': question, 'user_exist': user_exist})

def detail(request, question_id):
    """Create the dtail page."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

@login_required
def vote(request, question_id):
    """Update the vote for choice that have been voted."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if Vote.objects.filter(pk=question_id, user_id=request.user.id).exists():
            user_vote = question.vote_set.get(user=request.user)
            user_vote.choice = selected_choice
            user_vote.choice.votes += 1
            user_vote.choice.save()
            user_vote.save()
        else:
            selected_choice.vote_set.create(user=request.user, question=question)
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

@login_required
def vote_for_poll(request, question_id):
    """Check the poll is avalable to vote."""
    question = Question.objects.get(pk=question_id)
    if not(q.can_vote()):
        messages.error(request, "poll expires")
        return redirect('polls:index')
    return render(request, "polls/details.html", {"question": question})

def show_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_vote = Vote.objects.filter(pk=question_id, user_id=request.user.id)
    user_exist = Vote.objects.filter(pk=question_id, user_id=request.user.id).exists()
    return render(request, 'polls/results.html', {'question': question, 'user_vote': user_vote, 'user_exist': user_exist})

