from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_image'),
    path('upload_success/', views.upload_success, name="upload_success")
]
