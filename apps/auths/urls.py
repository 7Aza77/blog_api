from django.urls import path

from apps.auths.views import HealthCheckView

app_name: str = "auths"

urlpatterns: list = [
    path("health/", HealthCheckView.as_view(), name="health"),
]
