from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationAPIView, UserRetrieveUpdateAPIView, LoginView, IndexAPIView, logout_user, activate, index

app_name = 'authentication'
urlpatterns = [
    path('home/', IndexAPIView.as_view(), name='home'),
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_user),
]
