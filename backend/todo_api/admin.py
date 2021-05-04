from django.contrib import admin
from . import models

my_models = [models.Task, models.Color]
admin.site.register(my_models)
