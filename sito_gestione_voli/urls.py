from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='flys'),
    path('summary', views.summary, name='summary'),
    # path('admin_panel', views.admin_panel, name='admin_panel'),
    path('login', views.login_view, name='login'),
    path('process-selected-seats/', views.process_selected_seats, name='process_selected_seats'),
    path('confirmation/', views.confirmation_page, name='confirmation_page'),
    path('')
]
