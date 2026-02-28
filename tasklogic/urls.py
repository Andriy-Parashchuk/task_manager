from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks_list'),
    path('<int:pk>/update', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:folder_id>/create', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task'),

    path('folders/', TaskFolderListView.as_view(), name='task_folders_list'),
    path('folders/<int:pk>/update', TaskFolderUpdateView.as_view(), name='task_folder_update'),
    path('folders/<int:pk>/delete', TaskFolderDeleteView.as_view(), name='task_folder_delete'),
    path('folders/<int:pk>/', TaskListView.as_view(), name='task_list_by_folder'),
    path('registration/', UserCreationView.as_view(), name='registration'),

]
