from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Task, Color, SubTask
from .serializers import TaskSerializer, ColorSerializer, SubTaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(task__author=self.request.user)


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]