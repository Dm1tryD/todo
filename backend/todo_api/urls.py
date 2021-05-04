from django.urls import path
from rest_framework import routers

from .views import TaskViewSet, ColorViewSet

router = routers.SimpleRouter()
router.register(r'task', TaskViewSet)
router.register(r'color', ColorViewSet)

urlpatterns = []
urlpatterns += router.urls