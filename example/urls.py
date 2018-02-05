from django.urls import path

from example import flows

urlpatterns = [
    path('', flows.ExampleFlow().urls),
]
