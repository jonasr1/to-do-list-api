
from django.db.models.query import QuerySet
from django_filters import CharFilter, FilterSet

from .models import Task

STATUS_COMPLETED = "completed"
STATUS_PENDING = "pending"
STATUS_ALL = "all"


class TaskFilter(FilterSet):
    status = CharFilter(
        method="filter_by_status"
    )  # Alias para o campo is_completed

    class Meta:
        model = Task
        fields = ["status"]

    def filter_by_status(self, queryset: QuerySet, _name: str, status: str | None) -> QuerySet:  # noqa: E501
        filters = {
            STATUS_COMPLETED: self.filter_completed,
            STATUS_PENDING: self.filter_pending,
            STATUS_ALL: self.filter_all
        }
        return (
            filters.get(status.lower(), self.filter_none)(queryset)
            if status else queryset
        )

    def filter_completed(self, qs: QuerySet) -> QuerySet:
        return qs.filter(is_completed=True)

    def filter_pending(self, qs: QuerySet) -> QuerySet:
        return qs.filter(is_completed=False)

    def filter_all(self, qs: QuerySet) -> QuerySet:
        return qs

    def filter_none(self, qs: QuerySet) -> QuerySet:
        return qs.none()
