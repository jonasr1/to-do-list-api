from collections import Counter
from datetime import timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING, cast

from django.core.cache import cache
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.pagination import TaskPagination
from tasks.serializers import TaskSerializer
from tasks.services.statistics_service import calculate_task_stats

if TYPE_CHECKING:
    from users.models import User


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
    - You can filter tasks by their completion status using the 'status' query parameter in the URL: # noqa: E501
    - GET /tasks?status=completed will return only completed tasks.
    - GET /tasks?status=pending will return only pending tasks.
    - GET /tasks?status=all will return all tasks, regardless of their completion status.

    Sorting:
    - Sort by 'created_at' or 'title' using 'ordering':
        - GET /tasks?ordering=created_at
        - GET /tasks?ordering=-created_at
        - GET /tasks?ordering=title
        - GET /tasks?ordering=-title

    Pagination:
    - The results are paginated by default, returning 10 items per page.
    - You can adjust the number of items per page using the 'page_size' query parameter:
    - GET /tasks?page_size=20
    - The maximum allowed value for 'page_size' is 100.

    Additional Endpoints:
    - GET /tasks/stats/ → Retrieves task statistics (total, completed, pending, completion rate).
    - GET /tasks/metrics/?days=<n> → Retrieves the number of tasks created over the last `n` days.
    """  # noqa: E501

    serializer_class = TaskSerializer  # type: ignore[override]
    permission_classes = [IsAuthenticated]
    filter_backends = [  # type: ignore[override]
        DjangoFilterBackend,
        OrderingFilter,
    ]  # DjangoFilterBackend allows you to filter query results based on query parameters passed in the URL.  # noqa: E501
    pagination_class = TaskPagination  # pyrefly: ignore [bad-override]
    filterset_class = TaskFilter  # Here, it is configured to allow filtering by the 'is_completed' field.  # noqa: E501
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    @action(detail=False, url_path="stats")
    def get_task_stats(self, request: Request) -> Response:
        user = cast("User", request.user)
        cache_key = f"user_stats_{user.id}"
        if cached_data := cache.get(cache_key):
            return Response(cached_data)
        stats = calculate_task_stats(user).as_dict()
        cache.set(cache_key, stats, 300)
        return Response(stats)

    @method_decorator(cache_page(60 * 5, key_prefix=lambda r: f"user_{r.user.id}_metrics"))  # noqa: E501 # type: ignore
    @action(detail=False, url_path="metrics")
    def task_metrics(self, request: Request) -> Response:
        """
        Retrieve task creation statistics over a period of time.

        Query Parameters:
        - days (optional, default=7): Number of past days to consider.

        Example Request:
        GET /tasks/metrics?days=14

        Response format:
        {
            "days": 7,
            "task_distribution": {
                "10/02/2025": 3,
                "11/02/2025": 5,
                "12/02/2025": 2
            }
        }
        """
        try:
            days = int(request.query_params.get("days", 7))
            if days < 1:
                return Response(
                    {"error": '"days" parameter must be greater than 0'},
                    status=HTTPStatus.BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid days parameter"}, status=HTTPStatus.BAD_REQUEST
            )
        start_date = now() - timedelta(days=days)
        tasks = Task.objects.filter(user=request.user, created_at__gte=start_date)
        task_count_by_day = Counter(task.created_at.date() for task in tasks)
        ordered_metrics = {
            date.strftime("%d/%m/%Y"): count
            for date, count in sorted(task_count_by_day.items())
        }
        return Response(
            {"days": days, "task_distribution": ordered_metrics}, status=HTTPStatus.OK
        )

    def get_queryset(self) -> QuerySet:  # type: ignore
        cache_key = f"user_{self.request.user.id}_tasks"  # Unique key for each user
        if task_ids := cache.get(cache_key):
            return Task.objects.filter(id__in=task_ids)
        queryset = Task.objects.filter(user=self.request.user)
        cache.set(
            cache_key, list(queryset.values_list("id", flat=True)), timeout=300
        )  # 5 minute cache
        return queryset

    def perform_create(self, serializer: BaseSerializer) -> None:
        user = self.request.user
        title = serializer.validated_data.get("title")
        if Task.objects.filter(title=title, user=user).exists():
            raise ValidationError(
                {"title": ["A task with this title already exists for the user."]}
            )
        serializer.save(user=user)
