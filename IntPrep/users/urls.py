from django.urls import path
from .views import RegistrationView,LoginView,CurrentUserView

urlpatterns=[
    path('register/',RegistrationView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('me/',CurrentUserView.as_view(), name='user'),
]