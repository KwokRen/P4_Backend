from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import (ValidationError, PermissionDenied)
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.api.models import Task, Item
from apps.api.serializers import TaskSerializer, ItemSerializer


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all().filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        task = Task.objects.filter(
            name=request.data.get('name'),
            user=request.user
        )

        if task:
            message = 'Task already exists.'
            raise ValidationError(message)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all().filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        item = Item.objects.filter(
            name=request.data.get('name'),
            user=request.user
        )

        if item:
            message = 'Item already exists.'
            raise ValidationError(message)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)