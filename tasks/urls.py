from rest_framework.routers import DefaultRouter
from django.urls import path, include
from tasks.views import TaskHistoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(prefix=r'tasks', viewset=TaskViewSet, basename='task')
router.register(prefix=r'tasks-history', viewset=TaskHistoryViewSet, basename='task-history')

urlpatterns = [
    path('', include(router.urls))
]