from django.db import models
from django.contrib.auth.models import User


class Colour(models.Model):

    name = models.CharField(max_length=255)
    hex_color = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f'{self.name}, #{self.hex_color}'


class Task(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=510)
    color = models.ForeignKey(Colour, on_delete=models.PROTECT, related_name='color')
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created', 'completed']

    def __str__(self):
        return f'{self.author}, {self.text}'
