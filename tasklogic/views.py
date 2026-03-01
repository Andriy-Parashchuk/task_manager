from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .mixins import UserIsOwnerMixin
from django.db.models import Count, Q
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View

from .forms import *
from .models import *


class TaskListView(ListView):
    model = Task
    template_name = "tasks_list.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        if 'pk' in self.kwargs:
            self.task_folder = get_object_or_404(TaskFolder, pk=self.kwargs['pk'])
            return Task.objects.filter(folder=self.task_folder, user=self.request.user)
        else:
            try:
                return Task.objects.filter(user=self.request.user)
            except:
                return Task.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        if 'pk' in self.kwargs:
            context = super().get_context_data(**kwargs)
            context['folder'] = get_object_or_404(TaskFolder, pk=self.kwargs['pk'])
            context['folder_form'] = TaskFolderForm
            context['task_form'] = TaskForm
            return context
        else:
            return super().get_context_data(**kwargs)


class TaskDetailView(DetailView):
    model = Task
    template_name = "task.html"

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user  # Передаємо user у форму
            comment.task = self.get_object()  # Передаємо user у форму
            comment.save()
            return redirect('task', pk=self.get_object().pk)

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form_template.html'

    def form_valid(self, form):
        folder_id = self.kwargs.get('folder_id')
        folder = get_object_or_404(TaskFolder, id=folder_id)
        form.instance.folder = folder
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task_list_by_folder', kwargs={'pk': self.kwargs.get('folder_id')})


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'form_template.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаємо user у форму
        return kwargs

    def get_success_url(self):
        return reverse_lazy('task', kwargs={'pk': self.kwargs.get('pk')})


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = 'delete.html'

    def get_object(self):
        return Task.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('task_list_by_folder', kwargs={'pk': self.object.folder.id})


class TaskFolderListView(LoginRequiredMixin, ListView):
    model = TaskFolder
    template_name = 'folders.html'
    context_object_name = 'folders'

    def get_queryset(self):
        return TaskFolder.objects.filter(user=self.request.user)\
            .annotate(count_tasks=Count('tasks', filter=~Q(tasks__status='d')))
        # add annotate for count tasks and filter them by 'done' status using Q object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFolderForm
        return context

    def post(self, request, *args, **kwargs):
        form = TaskFolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = self.request.user  # Передаємо user у форму
            folder.save()
            return redirect('task_folders_list')
        return self.render_to_response(self.get_context_data(form=form))


class TaskFolderUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = TaskFolder
    form_class = TaskFolderForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse_lazy('task_list_by_folder', kwargs={'pk': self.kwargs.get('pk')})


class TaskFolderDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskFolder
    template_name = 'delete.html'
    success_url = reverse_lazy('task_folders_list')

    def get_object(self):
        return TaskFolder.objects.get(pk=self.kwargs['pk'])


class UserCreationView(CreateView):
    model = User
    template_name = 'registration/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('task_folders_list')


def logout_view(request):
    logout(request)
    return redirect('login')



