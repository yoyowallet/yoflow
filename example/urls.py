from django.conf.urls import url
from rest_framework import routers

from example import views


router = routers.SimpleRouter()
router.register(r'post', views.PostViewSet)

urlpatterns = router.urls + [
    url(r'^post-view/(?P<pk>[0-9]+)', views.approved_function_view),
    url(r'^post-cbv/(?P<pk>[0-9]+)', views.ApprovedClassBasedView.as_view()),
]
