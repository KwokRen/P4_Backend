from django.db import models
from apps.authentication.models import User


class Task(models.Model):

    class Meta:
        verbose_name_plural = 'tasks'

    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Item(models.Model):

    class Meta:
        verbose_name_plural = 'items'

    user = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
