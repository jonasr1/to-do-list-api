from typing import cast
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

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
    filterset_fields = ['is_completed'] # Here, it is configured to allow filtering by the 'is_completed' field
    
    def get_queryset(self): # type: ignore
        request = cast(Request, self.request)
        queryset = self.queryset.filter(user=request.user) # Filter tasks by the authentucated user
        status = request.query_params.get('status', '')
        filters = {
            'completed': lambda qs: qs.filter(is_completed=True),
            'pending': lambda qs: qs.filter(is_completed=False),
            'all': lambda qs: qs
        }
        return filters.get(status.lower(), lambda qs: qs.none())(queryset) if status else queryset
    
    def perform_create(self, serializer): # type: ignore
        user = self.request.user
        title = serializer.validated_data.get('title')
        if Task.objects.filter(title=title, user=user).exists():
            raise ValidationError({'title': ['A task with this title already exists for the user.']})
        serializer.save(user=user)
