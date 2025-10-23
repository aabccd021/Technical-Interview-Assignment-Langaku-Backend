from django.urls import path

from assignment.views import initialize_data

urlpatterns = [path("init_data/", initialize_data, name="initialize_data")]
