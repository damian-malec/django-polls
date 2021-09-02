from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Choice, Question, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(question=self.object.id)
        context['question_list'] = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]
        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_list_results'] = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]
        return context


class VoteView(View):

    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, "Nie wybrałeś żadnej opcji!")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))
        else:
            selected_choice.votes += 1
            selected_choice.save()
            messages.success(request, "Brawo, głos został oddany!")
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
            messages.success(request, "Brawo, dodałeś komentarz!")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))
        return render(request, self.template_name, {'question': question, 'form': form})


class DeleteCommentView(View):

    @method_decorator(login_required)
    def post(self, request, slug):
        comment = get_object_or_404(Comment, id=slug)
        comment.delete()
        return HttpResponseRedirect(reverse('polls:detail', args=(comment.question.slug,)))
        pass