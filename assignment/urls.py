from django.urls import path

from assignment.views import recordsjson, user_summary

urlpatterns = [
    path("recordsjson", recordsjson),
    path("users/<str:user_id>/summary", user_summary),
]
