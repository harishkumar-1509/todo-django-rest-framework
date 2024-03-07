from django.db import models
from accounts.models import User
from constants import *

# Create your models here.
class TodoCategory(models.Model):
    user = models.ForeignKey(User,related_name="categoryuser",on_delete = models.CASCADE)
    category_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = "todo_category"
        verbose_name = "category"
        verbose_name_plural = "categories"

class TodoTask(models.Model):
    # PRIORITY_CHOICES = [
    #     ('P1', 'P1'),
    #     ('P2', 'P2'),
    #     ('P3', 'P3'),
    #     ('P4', 'P4'),
    # ]
    
    # TASK_STATUS_CHOICES = [
    #     ('Open', 'Open'),
    #     ('In Progress', 'In Progress'),
    #     ('Completed', 'Completed'),
    # ]

    user = models.ForeignKey(User,related_name="taskuser",on_delete = models.CASCADE)
    task_name = models.CharField(max_length=155)
    task_description = models.TextField(max_length=400)
    task_category = models.ForeignKey(TodoCategory,related_name="taskcategory",on_delete=models.DO_NOTHING)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='P1')
    task_status = models.CharField(max_length=15, choices=TASK_STATUS_CHOICES, default='Open')
    starred = models.BooleanField(default=False)
    task_start_date = models.DateTimeField(null=True)
    task_end_date = models.DateTimeField(null=True)
    task_time_log = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.task_name
    
    class Meta:
        db_table = "todo_task"
        verbose_name = "todo task"
        verbose_name_plural = "todo tasks"

class TodoSubTask(models.Model):
    # TASK_STATUS_CHOICES = [
    #     ('Open', 'Open'),
    #     ('In Progress', 'In Progress'),
    #     ('Completed', 'Completed'),
    # ]
    
    task = models.ForeignKey(TodoTask, related_name="subtasks", on_delete = models.CASCADE)
    subtask_name = models.CharField(max_length=155)
    subtask_description = models.TextField(max_length=400)
    subtask_status = models.CharField(max_length=15, choices=TASK_STATUS_CHOICES, default='Open')
    subtask_start_date = models.DateTimeField(null=True)
    subtask_end_date = models.DateTimeField(null=True)
    subtask_time_log = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subtask_name
    
    class Meta:
        db_table = "todo_sub_task"
        verbose_name = "todo sub task"
        verbose_name_plural = "todo sub tasks"