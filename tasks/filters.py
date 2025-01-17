from django_filters import rest_framework as filters

from tasks.models import Task

class TaskFilter(filters.FilterSet):
    status = filters.CharFilter(method='filter_by_status') # Alias para o campo is_completed

    class Meta:
        model = Task
        fields = ['status']
        
    def filter_by_status(self, queryset, name, status):
        filters = {
            'completed': lambda qs: qs.filter(is_completed=True),
            'pending': lambda qs: qs.filter(is_completed=False),
            'all': lambda qs: qs
        }
        return filters.get(status.lower(), lambda qs: qs.none())(queryset) if status else queryset