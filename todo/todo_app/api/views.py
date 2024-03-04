from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from .serializers import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

# API:1 -> Create and list a category/categories for the user
# API:2 -> Create and list a tasks along with subtasks for the user
# API:3 -> Create a subtask for the user

class CreateListCategoryView(generics.ListCreateAPIView):
    model = TodoCategory
    serializer_class = TodoCategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TodoCategory.objects.filter(user=self.request.user).order_by('category_name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreateListTasksView(generics.ListCreateAPIView):
    model = TodoTask
    permission_classes = [IsAuthenticated]
    serializer_class = TodoTaskSerializer
    
    def get_queryset(self):
        return TodoTask.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        no_of_categories = TodoCategory.objects.filter(user=self.request.user).count()
        if len(no_of_categories) == 0:
            return Response(data= {"msg":"You need to create a new category to create a new task"})
        serializer.save(user=self.request.user)
    
    def get_serializer_context(self):
        # Pass any additional context data here
        context = super().get_serializer_context()
        # Add your context data as key-value pairs
        context['user'] = self.request.user
        return context

class CreateSubTask(generics.CreateAPIView):
    model = TodoSubTask
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSubTaskSerializer

class PendingTasksView(generics.ListAPIView):
    model = TodoTask
    permission_classes = [IsAuthenticated]
    serializer_class = TodoTaskSerializer
    
    def get_queryset(self):
        last_days = self.request.query_params.get('last_days')
        
        if last_days:
            # To get the start date from the last days specified 
            start_date = timezone.now() - timedelta(days=int(last_days))
        else:
            # To get start date as the date 365 days before the current date
            start_date = start_date = timezone.now() - timedelta(days=365)
        
        # in_progress_tasks = TodoTask.objects.filter(
        #     user = self.request.user,
        #     task_status = 'In Progress',
        #     created_at__gt = start_date
        # )
        
        # open_tasks = TodoTask.objects.filter(
        #     user = self.request.user,
        #     task_status = 'Open',
        #     created_at__gt = start_date
        # )
        
        pending_tasks = TodoTask.objects.filter(
            Q(user = self.request.user,
              task_status = 'In Progress',
              created_at__gt = start_date) | 
            Q(
                user = self.request.user,
                task_status = 'Open',
                created_at__gt = start_date
            ))
        
        # return in_progress_tasks.union(open_tasks)
        return pending_tasks
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
        
        
        


