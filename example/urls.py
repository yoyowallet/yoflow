from django.urls import re_path
from rest_framework import routers

from example import views

router = routers.SimpleRouter()
router.register(r'post', views.PostViewSet)

urlpatterns = router.urls + [
    re_path(r'^post-view/(?P<pk>[0-9]+)', views.approved_function_view),
    re_path(r'^post-cbv/(?P<pk>[0-9]+)', views.ApprovedClassBasedView.as_view()),
]
