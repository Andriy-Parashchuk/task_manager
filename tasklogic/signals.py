from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TaskFolder


@receiver(post_save, sender=User)
def create_task_category(sender, instance, created, **kwargs):
    if created:
        TaskFolder.objects.create(user=instance, is_default=True, title='My tasks')

