from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('autor', 'tekst',)


class ChoiceForm(forms.Form):
    choice_text = forms.ChoiceField(choices=(
        ('1', 'test1'),
        ('2', 'test2'),
        ('3', 'test3'),
        ('4', 'test4'),
    ))

    class Meta:
        fields = ('choice_text',)

        widgets = {
            'choice_text': forms.RadioSelect(attrs={'class': 'form-control'}),
        }