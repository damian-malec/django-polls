import datetime

from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.urls import reverse


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'slug': self.slug})

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    autor = models.CharField(max_length=200)
    tekst = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return 'Komentarz {} autorstwa {}'.format(self.tekst, self.autor)