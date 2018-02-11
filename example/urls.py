from django.urls import path

from example import flows

urlpatterns = [
    path('parent/', flows.ParentFlow().urls, name='parent'),
    path('child/', flows.ChildFlow().urls, name='child'),
]
