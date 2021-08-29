from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Choice, Question, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(question=self.object.id)
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class VoteView(View):

    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "Nie wybrałeś żadnej opcji.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.slug,)))


class CommentView(generic.FormView):
    form_class = CommentForm
    template_name = 'polls/detail.html'

    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))
        return render(request, self.template_name, {'question': question, 'form': form})


class DeleteCommentView(View):

    @method_decorator(login_required)
    def post(self, request, slug):
        comment = get_object_or_404(Comment, id=slug)
        comment.delete()
        return HttpResponseRedirect(reverse('polls:detail', args=(comment.question.slug,)))
        pass