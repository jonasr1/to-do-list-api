from rest_framework.routers import DefaultRouter

from tasks.views import TaskViewSet

router = DefaultRouter()
router.register(prefix=r'tasks', viewset=TaskViewSet)

urlpatterns = router.urls

