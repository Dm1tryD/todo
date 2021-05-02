from django.contrib import admin
from . import models

my_models = [models.Task, models.Colour]
admin.site.register(my_models)
