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
    return render(request, 'polls/results.html', {'question': question})

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
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    context = {'latest_question_list': latest_question_list, }
    return HttpResponse(template.render(context, request))

@login_required
def vote_for_poll(request, pk):
    """Check the poll is avalable to vote."""
    q = Question.objects.get(pk=pk)
    if not(q.can_vote()):
        messages.error(request, "poll expires")
        return redirect('polls:index')
    return render(request, "polls/details.html", {"question": q})
