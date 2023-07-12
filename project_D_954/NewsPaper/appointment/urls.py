from django.urls import path, include

from .views import AppointmentView

urlpatterns = [
    path('', AppointmentView.as_view(), name='appointments'),

]