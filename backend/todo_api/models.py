from django.db import models
from django.contrib.auth.models import User

from todo_rest import settings


class Color(models.Model):

    name = models.CharField(max_length=255)
    hex_color = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f'{self.name}, #{self.hex_color}'


class Task(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=510)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='color')
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created', 'completed']

    def __str__(self):
        return f'{self.author}, {self.text}'


class SubTask(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task')
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task.author}, {self.text}'
