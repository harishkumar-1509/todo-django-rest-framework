from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from .serializers import *

# Create your views here.

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
        categories = TodoCategory.objects.filter(user=self.request.user)
        if len(categories) == 0:
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
    
        
        
        


