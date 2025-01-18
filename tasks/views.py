from .pagination import TaskPagination
from rest_framework.filters import OrderingFilter
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
from django.db.models import Count, Q


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
    
    Sorting:
    - You can sort the tasks by 'createdAt' or 'title' using the 'ordering' query parameter in the URL.
    - GET /tasks?ordering=created_at|title
    
    Pagination:
    - The results are paginated by default, returning 10 items per page.
    - You can adjust the number of items per page using the 'page_size' query parameter:
    - GET /tasks?page_size=20
    - The maximum allowed value for 'page_size' is 100.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter] # DjangoFilterBackend allows you to filter query results based on query parameters passed in the URL.
    filterset_class = TaskFilter # Here, it is configured to allow filtering by the 'is_completed' field
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    pagination_class = TaskPagination

    @action(detail=False, url_path='stats')
    def get_task_stats(self, request: Request) -> Response:
        user = request.user
        stats = Task.objects.filter(user=user).aggregate(
            total_tasks=Count('id'),
            completed_tasks=Count('id', filter=Q(is_completed=True)),
        )
        total_tasks = stats['total_tasks']
        completed_tasks = stats['completed_tasks']
        pending_tasks = total_tasks - completed_tasks
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        result = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_percentage': f'{completion_percentage}%' if completion_percentage!=0 else f'0%'
        }
        return Response(result)
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer): # type: ignore
        user = self.request.user
        title = serializer.validated_data.get('title')
        if Task.objects.filter(title=title, user=user).exists():
            raise ValidationError({'title': ['A task with this title already exists for the user.']})
        serializer.save(user=user)
