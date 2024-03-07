from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from .serializers import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.http import Http404
from .pagination import *

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
    pagination_class = TodoTaskListPagination
    
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

class RetrieveUpdateDeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk, request):
        try:
            return TodoTask.objects.get(pk=pk, user=request.user)
        except TodoTask.DoesNotExist:
            raise Http404("Todo task does not exist")
               
    def get(self,request,pk):
        task = self.get_object(pk, request)
        serializer = TodoTaskSerializer(task)
        return Response(serializer.data)
    
    def put(self,request,pk):
        task = self.get_object(pk, request)
        serializer = TodoTaskSerializer(task, data=request.data)
        task_status = request.data.get('task_status')
        task_start_date = request.data.get('task_start_date')
        task_end_date = request.data.get('task_end_date')
        task_time_log = request.data.get('task_time_log')
        
        if len(task_time_log) is not 0:
            valid_time_format = TodoUtils.validate_time_string(task_time_log)
            if not valid_time_format:
                return Response({'msg': 'Task time log is not valid please check the format or the values'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            sub_tasks = TodoSubTask.objects.filter(task=task)
            """If the task has 1 or more sub tasks associated with it and the user wants to complete the task, 
            then we need to check any of the sub tasks in the task has in progress or open status and deny the user to complete the main task if any."""
            if task_status == "Completed":
                if sub_tasks.count() > 0:
                    for sub_task in sub_tasks:
                        if sub_task.subtask_status == "Open" or sub_task.subtask_status == "In Progress":
                            return Response({'msg': 'Cannot complete task because it has sub tasks that are not completed!'}, status=status.HTTP_400_BAD_REQUEST)
            
                # Check whether the user has given start date and end date , only if given they can close the task
                if task_start_date is None:
                    return Response({'msg': 'Task start date is required to end task!'}, status=status.HTTP_400_BAD_REQUEST)
                
                if task_end_date is None:
                    return Response({'msg': 'Task end date is required to end task!'}, status=status.HTTP_400_BAD_REQUEST)
                
                if task_time_log is None or "":
                    return Response({'msg': 'Task time log is required to end task!'}, status=status.HTTP_400_BAD_REQUEST)
                
                valid_time_format = TodoUtils.validate_time_string(task_time_log)
                if not valid_time_format:
                    return Response({'msg': 'Task time log is not valid please check the format or the values'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        task = self.get_object(pk, request)
        sub_tasks = TodoSubTask.objects.filter(task=task)
        for sub_task in sub_tasks:
            if sub_task.subtask_status == "In Progress":
                return Response({'msg': 'Task cannot be deleted because it has a sub task in progress!'})
        task.delete()
        return Response({'msg': 'Task deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
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

class RetrieveUpdateDeleteSubTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk, request):
        try:
            return TodoSubTask.objects.get(pk=pk)
        except TodoSubTask.DoesNotExist:
            raise Http404("Sub task does not exist")
    def get(self, request,pk):
        sub_task = self.get_object(pk, request)
        serializer = TodoSubTaskSerializer(sub_task)
        return Response(serializer.data)
    
    def put(self, request,pk):
        sub_task = self.get_object(pk, request)
        serializer = TodoSubTaskSerializer(sub_task, data=request.data)
        subtask_status = request.data.get('subtask_status')
        subtask_start_date = request.data.get('subtask_start_date')
        subtask_end_date = request.data.get('subtask_end_date')
        task_time_log = request.data.get('subtask_time_log')
        
        if len(task_time_log) is not 0:
            valid_time_format = TodoUtils.validate_time_string(task_time_log)
            if not valid_time_format:
                return Response({'msg': 'Task time log is not valid please check the format or the values'}, status=status.HTTP_400_BAD_REQUEST)
            
        if serializer.is_valid():
            if subtask_status == "Completed":
                if subtask_start_date is None:
                    return Response({'msg': 'Sub-Task start date is required to end task!'}, status=status.HTTP_400_BAD_REQUEST)
                if subtask_end_date is None:
                    return Response({'msg': 'Sub-Task end date is required to end task!'}, status=status.HTTP_400_BAD_REQUEST)
                if task_time_log is None or "":
                    return Response({'msg': 'Task time log is required to end task!'}, status=status.HTTP_400_BAD_REQUEST)
                
                valid_time_format = TodoUtils.validate_time_string(task_time_log)
                if not valid_time_format:
                    return Response({'msg': 'Task time log is not valid please check the format or the values'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        sub_task = self.get_object(pk, request)
        if sub_task.subtask_status == "In Progress":
            return Response({'msg': 'In Progress Sub-Task cannot be deleted!'}, status=status.HTTP_400_BAD_REQUEST)
        sub_task.delete()
        return Response({'msg': 'Sub-Task deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
        
        


