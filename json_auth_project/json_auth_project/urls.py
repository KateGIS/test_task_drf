from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls', namespace='authentication')),
    path('events/', include(('event.urls', 'event'), namespace='event')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', RedirectView.as_view(url='/api/home/')),
]
