# urls.py
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, get_csrf_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
]
