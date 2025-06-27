from django.contrib import admin
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.urls import include, path


def health_check(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "OK"})

urlpatterns = [
    path("health/", health_check),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include("tasks.urls"))
]
