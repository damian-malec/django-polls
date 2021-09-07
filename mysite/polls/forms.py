from django import forms
from .models import Comment, Choice

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('autor', 'tekst',)


class ChoiceForm(forms.ModelForm):
    choice_text = forms.ChoiceField(choices=(
        ('1', 'opcja 1'),
        ('2', 'opcja 2'),
        ('3', 'opcja 3'),
    ),
        widget=forms.RadioSelect(attrs={'id': 'value'})
    )

    class Meta:
        model = Choice
        fields = ('choice_text',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # self.fields['choice_text'].choices = [('1','xxx')]