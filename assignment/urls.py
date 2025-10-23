from django.urls import path

from assignment.views import recordsjson

urlpatterns = [path("recordsjson", recordsjson)]
