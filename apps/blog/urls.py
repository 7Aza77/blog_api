from django.urls import path

from apps.blog.views import BlogHealthCheckView

app_name: str = "blog"

urlpatterns: list = [
    path("health/", BlogHealthCheckView.as_view(), name="health"),
]
