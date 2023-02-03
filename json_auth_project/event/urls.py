from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from rest_framework import routers

app_name = 'event'
urlpatterns = [
    path('tag/', views.TagList.as_view(), name="tag"),
    path('event/', views.EventList.as_view(), name="event"),
    path('event/create/', views.EventCreate.as_view(), name="event_create"),
    path('event/<int:pk>/', views.EventDetail.as_view(), name= "event_detail")
]
