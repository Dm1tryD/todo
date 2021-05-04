from rest_framework import serializers
from . import models


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'hex_color'
        )
        model = models.Color


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.Task