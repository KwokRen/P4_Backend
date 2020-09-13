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


class TaskItems(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    def get_queryset(self):
        try:
            if self.kwargs.get("task_pk"):
                task = Task.objects.get(pk=self.kwargs["task_pk"])
                queryset = Item.objects.filter(
                    task=task,
                    user=self.request.user
                )
                if not queryset:
                    raise ValidationError("You do not have access to this task.")
                else:
                    return queryset
        except Task.DoesNotExist:
            raise ValidationError('You do not have access to this task.')


    def create(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.request.data['task']):
                return super().create(request)
        except Task.DoesNotExist:
            raise ValidationError('You cannot create the item in this task.')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OneItem(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    def get_queryset(self):
        try:
            if self.kwargs.get("task_pk") and self.kwargs.get("pk"):
                task = Task.objects.get(pk=self.kwargs["task_pk"])
                queryset = Item.objects.filter(
                    task=task,
                    user=self.request.user,
                    pk=self.kwargs["pk"]
                )
                return queryset
        except Task.DoesNotExist:
            raise ValidationError("You cannot access a item that doesn't exist")

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.request.data['task']):
                return super().update(request, *args, **kwargs)
        except Task.DoesNotExist:
            raise ValidationError("You cannot update the item in this task.")

    def destroy(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.kwargs['task_pk']):
                return super().destroy(request, *args, **kwargs)
        except Task.DoesNotExist:
            raise ValidationError("You cannot delete the item in this task.")