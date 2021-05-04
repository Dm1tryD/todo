from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from .models import Task, Color
from .serializers import TaskSerializer, ColorSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
