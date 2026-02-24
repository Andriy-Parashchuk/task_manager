from django.forms import ModelForm, DateTimeInput, HiddenInput

from .models import *


class TaskFolderForm(ModelForm):
    class Meta:
        model = TaskFolder
        fields = ['title']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'start_estimate',
            'end_estimate',
        ]

        widgets = {
            'start_estimate' : DateTimeInput(attrs={'type': 'datetime-local'}),
            "end_estimate": DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'start_estimate',
            'end_estimate',
            'folder'
        ]

        widgets = {
            'start_estimate': DateTimeInput(attrs={'type': 'datetime-local'}),
            "end_estimate": DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Отримуємо користувача з представлення
        super().__init__(*args, **kwargs)
        if user:
            self.fields['folder'].queryset = TaskFolder.objects.filter(user=user)  # Фільтруємо папки


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]

