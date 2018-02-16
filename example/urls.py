from django.conf.urls import url

from example import flows

urlpatterns = [
    url(r'^parent/', flows.ParentFlow().urls, name='parent'),
    url(r'^child/', flows.ChildFlow().urls, name='child'),
]
