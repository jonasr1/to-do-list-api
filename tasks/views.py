from typing import cast
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage tasks.
    Supports:
    - Create a new task (POST /tasks)
    - List all tasks (GET /tasks)
    - Update a specific task (PUT /tasks/:id)
    - Delete a specific task (DELETE /tasks/:id)
    - Toggle a task's completion status (PATCH /tasks/:id)
    
    Filtering:
    - You can filter tasks by their completion status using the 'status' query parameter in the URL:
    - GET /tasks?status=completed will return only completed tasks.
    - GET /tasks?status=pending will return only pending tasks.
    - GET /tasks?status=all will return all tasks, regardless of their completion status.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend] # DjangoFilterBackend allows you to filter query results based on query parameters passed in the URL.
    filterset_class = TaskFilter # Here, it is configured to allow filtering by the 'is_completed' field
    
    @action(detail=False, url_path='stats')
    def get_task_stats(self, request: Request) -> Response:
        user = request.user
        total_tasks = Task.objects.filter(user=user).count()
        completed_tasks = Task.objects.filter(user=user, is_completed=True).count()
        pending_tasks = total_tasks - completed_tasks
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        stats = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_percentage': completion_percentage
        }
        return Response(stats)
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer): # type: ignore
        user = self.request.user
        title = serializer.validated_data.get('title')
        if Task.objects.filter(title=title, user=user).exists():
            raise ValidationError({'title': ['A task with this title already exists for the user.']})
        serializer.save(user=user)
