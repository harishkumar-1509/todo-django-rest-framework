from rest_framework import serializers
from ..models import *

class TodoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCategory
        fields = ['id', 'user', 'category_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TodoSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoSubTask
        fields = ['id', 'subtask_name', 'subtask_description', 'subtask_category', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TodoTaskSerializer(serializers.ModelSerializer):
    subtasks = TodoSubTaskSerializer(many=True, read_only=True)  # Nested Serializer for Subtasks
    
    class Meta:
        model = TodoTask
        fields = ['id', 'user', 'task_name', 'task_description', 'task_category', 'created_at', 'updated_at', 'subtasks']
        read_only_fields = ['created_at', 'updated_at']