from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html' # mudando o nome do template disponibilizado pela view, pois o padrão seria <model_name>_list.html
    context_object_name = 'latest_question_list' # mudando o nome do objeto disponibilizado para o template

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future).."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question # necessário especificar o model para o template de detalhe
    template_name = 'polls/detail.html' # mudando o nome do template disponibilizado pela view, pois o padrão seria <model_name>_list.html

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
        

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # request.POST is a dict like request.GET
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) # reverse method to concatenate args in url
