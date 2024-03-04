from rest_framework import serializers
from ..models import *

class TodoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCategory
        fields = ['id', 'category_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TodoSubTaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=TodoTask.objects.all())
    class Meta:
        model = TodoSubTask
        fields = ['id','task', 'subtask_name','subtask_status', 'subtask_description', 'subtask_start_date','subtask_end_date','created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at','task','id']

class TodoTaskSerializer(serializers.ModelSerializer):
    subtasks = TodoSubTaskSerializer(many=True, read_only=True)  # Nested Serializer for Subtasks
    no_of_sub_tasks_completed = serializers.SerializerMethodField()
    no_of_pending_sub_tasks = serializers.SerializerMethodField()
    class Meta:
        model = TodoTask
        fields = ['id', 'task_name', 'task_description', 'task_category', 'created_at', 'updated_at', 'subtasks','task_start_date', 'task_end_date','task_status','priority',
                  'no_of_sub_tasks_completed','no_of_pending_sub_tasks']
        read_only_fields = ['created_at', 'updated_at','id']
    
    def get_no_of_sub_tasks_completed(self,obj):
        # user = self.context.get('user')
        # return TodoTask.objects.filter(task_status="Completed",user=user).count()
        subtasks = obj.subtasks.all()
        count = 0
        for task in subtasks:
            if task.subtask_status == 'Completed':
                count+=1
        return count
    
    def get_no_of_pending_sub_tasks(self,obj):
        # user = self.context.get('user')
        subtasks = obj.subtasks.all()
        no_of_inprogress_tasks = 0
        no_of_open_tasks = 0
        
        for task in subtasks:
            if task.subtask_status == 'Open':
                no_of_open_tasks+=1
                
        for task in subtasks:
            if task.subtask_status == 'In Progress':
                no_of_inprogress_tasks+=1   
                    
        return no_of_inprogress_tasks+no_of_open_tasks