from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('send-contact-email/', views.send_contact_email, name='send_contact_email'),
]
