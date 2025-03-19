from django.urls import path

from src.api.routes import api

urlpatterns = [
    path("api/", api.urls),
]
