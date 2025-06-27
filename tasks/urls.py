from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import TaskHistoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(prefix=r"tasks", viewset=TaskViewSet, basename="task")  # type: ignore[bad-argument-type]
router.register(
    prefix=r"tasks-history", viewset=TaskHistoryViewSet, basename="task-history"  # type: ignore[bad-argument-type]
)

urlpatterns = [path("", include(router.urls))]
