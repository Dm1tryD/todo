from rest_framework import serializers
from . import models


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'hex_color'
        )
        model = models.Color


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'color',
            'completed'
        )
        model = models.Task
        read_only_fields = ('author',)


class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.SubTask