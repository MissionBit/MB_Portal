from django.urls import path
from . import views

urlpatterns = [		
        path('', views.donor, name='donor'),
]
