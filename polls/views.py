from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.views import generic, View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Question, Comment
from .forms import CommentForm, ChoiceForm


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
        context['form_vote'] = ChoiceForm()
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


class VoteView(generic.FormView):
    form_class = ChoiceForm
    template_name = 'polls/detail.html'

    # def form_valid(self, form):
    #     selected_choice = form.cleaned_data.get['choice_text']
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     messages.success(self.request, "Brawo, głos został oddany!")
    #     return super(VoteView, self).form_valid(form)
    #
    # def form_invalid(self, form):
    #     messages.error(self.request, "Nie wybrałeś żadnej opcji!")
    #     return HttpResponseRedirect(reverse('polls:detail', args=(self.question.slug,)))
    #
    # def post(self, request, slug, *args, **kwargs):
    #     self.question = get_object_or_404(Question, slug=slug)
    #     return super(VoteView, self).post(request, *args, **kwargs)

    def post(self, request, slug, *args, **kwargs):
        question = get_object_or_404(Question, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            # selected_choice = form.cleaned_data['choice_text']
            # ...
            messages.success(request, "Brawo, głos został oddany!")
            return HttpResponseRedirect(reverse('polls:results', args=(question.slug,)))
        else:
            messages.error(request, "Nie wybrałeś żadnej opcji!")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))
        return render(request, self.template_name, {'question':question, 'form':form})


class CommentView(generic.FormView):
    form_class = CommentForm
    template_name = 'polls/detail.html'

    def post(self, request, slug, **kwargs):
        question = get_object_or_404(Question, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            messages.success(request, "Brawo, dodałeś komentarz!")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))
        else:
            messages.error(request, "Wypełnij wszystkie pola, żeby dodać komentarz.")
            return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))
        return render(request, self.template_name, {'question': question, 'form': form})


class DeleteCommentView(View):

    @method_decorator(login_required)
    def post(self, request, slug):
        comment = get_object_or_404(Comment, id=slug)
        comment.delete()
        messages.warning(request, "Komentarz został pomyślnie usunięty.")
        return HttpResponseRedirect(reverse('polls:detail', args=(comment.question.slug,)))
        pass
