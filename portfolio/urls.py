from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('send-contact-email/', views.send_contact_email, name='send_contact_email'),
]
