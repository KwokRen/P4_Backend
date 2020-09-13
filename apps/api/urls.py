from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from apps.api.views import TaskViewSet
router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = router.urls
