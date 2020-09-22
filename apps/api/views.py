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

    # Grabbing all tasks
    def get_queryset(self):
        queryset = Task.objects.all().filter(user=self.request.user).order_by('created_at')
        return queryset
    # Creating a task

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

    # Removing a task
    def destroy(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        if not request.user == task.user:
            raise PermissionDenied("You cannot delete this task")
        super().destroy(request, *args, **kwargs)
        return Response({
            "message": "Successfully deleted task"
        })


class TaskItems(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    # Listing all the items within a task
    def get_queryset(self):
        try:
            if self.kwargs.get("task_pk"):
                task = Task.objects.get(pk=self.kwargs["task_pk"])
                queryset = Item.objects.filter(
                    task=task,
                    user=self.request.user
                ).order_by('created_at')
                if not queryset:
                    raise ValidationError("You do not have access to this task.")
                else:
                    return queryset
        except Task.DoesNotExist:
            raise ValidationError('You do not have access to this task.')

    # Creating an item
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

    # Getting all items
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

    # Updating an item
    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.request.data['task']):
                return super().update(request, *args, **kwargs)
        except Task.DoesNotExist:
            raise ValidationError("You cannot update the item in this task.")

    # Deleting an item
    def destroy(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.kwargs['task_pk']):
                super().destroy(request, *args, **kwargs)
                return Response({
                    "message": "Successfully deleted item"
                })
        except Task.DoesNotExist:
            raise ValidationError("You cannot delete the item in this task.")