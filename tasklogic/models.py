from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TaskFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_folder')
    title = models.CharField(max_length=100, default='My tasks')
    is_default = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise ValueError("Не можна видалити дефолтну категорію")
        else:
            default_folder = TaskFolder.objects.get(user=self.user, is_default=True)
            Task.objects.filter(folder=self).update(folder=default_folder)  # Переносимо завдання
            super().delete(*args, **kwargs)  # Видаляємо категорію

    def __str__(self):
        return f'{self.user.username} - {self.title}'


class Task(models.Model):
    PRIORITY_VARIANTS = {
        "h": "high",
        "m": "medium",
        "l": "low"
    }

    STATUS_VARIANTS = {
        "d": "done",
        "w": "in_work",
        "f": "free"
    }

    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    folder = models.ForeignKey(TaskFolder, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_VARIANTS)
    priority = models.CharField(max_length=1, choices=PRIORITY_VARIANTS)
    start_estimate = models.DateTimeField()
    end_estimate = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username}: {self.title}, {self.status}, {self.priority}'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.pk:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super().save(*args, **kwargs)
