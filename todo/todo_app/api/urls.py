from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', CreateListTasksView.as_view(), name='task-list-create'),
    path('categories/', CreateListCategoryView.as_view(), name='category-list-create'),
    # path('tasks/<int:pk>/', TodoTaskDetailView.as_view(), name='task-detail'),
    path('subtasks/', CreateSubTask.as_view(), name='subtask-create'),
    # path('subtasks/<int:pk>/', TodoSubTaskDetailView.as_view(), name='subtask-detail'),
    path('get-pending-tasks/', PendingTasksView.as_view(), name='get-pending-tasks'),
    path('get-specific-task/<int:pk>', RetrieveUpdateDeleteTaskView.as_view(), name='get-specific-task'),
]
