from django.contrib import admin
from django.conf.urls import include, url


urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^blog/', include('example.urls')),
]
