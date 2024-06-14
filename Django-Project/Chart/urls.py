from django.urls import path
from . import views
urlpatterns = [
    path('chart/', views.cost_diagram, name = "cost_diagram")
]
