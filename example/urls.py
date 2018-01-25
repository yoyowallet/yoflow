from django.urls import path

from example import flows

urlpatterns = [
    path('<int:pk>/', flows.ExampleFlow().urls),
]
