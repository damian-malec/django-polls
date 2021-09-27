from django import forms
from .models import Comment, Choice

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('autor', 'tekst',)


class ChoiceForm(forms.Form):

    choice_text = forms.ChoiceField(choices=(
        ('1', 'opcja 1'),
        ('2', 'opcja 2'),
        ('3', 'opcja 3'),
    ),
        widget=forms.RadioSelect(attrs={'class': 'ChoiceForm', 'placeholder': 'Your choice',})
    )

    # class Meta:
    #     model = Choice
    #     fields = ('choice_text',)
    #     widgets = {'choice_text': forms.RadioSelect(attrs={'class': 'ChoiceForm', 'placeholder': 'Your choice',})}

        # def __init__(self, *args, **kwargs):
        #    super().__init__(*args, **kwargs)
        #    self.fields['choice_text'].choices = [('1','xxx')]
