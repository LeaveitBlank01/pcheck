from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'main_app'

urlpatterns = [
    path('add-pc/', views.add_pc, name='add-pc'),
    path('delete-pc/<int:pk>/', views.delete_pc, name='delete-pc'),
    path('add-pc-from-form/', views.add_pc_from_form, name='add-pc-from-form'),
    path('pc-list/', views.PCListView.as_view(), name='pc-list'),
    path('pc-detail/<int:pk>/', views.PCDetailView.as_view(), name='pc-detail'),
    path('pc-update/<int:pk>/', views.PCUpdateView.as_view(), name='pc-update'),
    path('ping-ip/<int:pk>/', views.ping_ip_address, name='ping-ip'),
    path('ajax/get-ping-data/', views.get_ping_data, name='get-ping-data'),
    path('ajax/verify-pc-name/', views.verify_pc_name, name='verify-pc-name'),
    path('ajax/verify-pc-ip-address/', views.verify_pc_ip_address, name='verify-pc-ip-address'),
    path('ajax/get-pc-details/<int:pk>/', views.get_pc_details, name='get-pc-details'),
]