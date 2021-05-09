from django.urls import path
from rest_framework import routers

from .views import TaskViewSet, ColorViewSet, SubTaskViewSet

router = routers.SimpleRouter()
router.register(r'task', TaskViewSet)
router.register(r'color', ColorViewSet)
router.register(r'subtask', SubTaskViewSet)

urlpatterns = []
urlpatterns += router.urls