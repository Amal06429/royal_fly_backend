from django.urls import path
from . import views

urlpatterns = [
    # Enquiry endpoints
    path('enquiries/', views.enquiry_list, name='enquiry-list'),
    path('enquiries/create/', views.create_enquiry, name='enquiry-create'),
    
    # Flight endpoints
    path('flights/', views.flights_api, name='flights-list-create'),
    path('flights/<int:pk>/update/', views.update_flight, name='flight-update'),
    path('flights/<int:pk>/', views.delete_flight, name='flight-delete'),
    
    # Dashboard endpoint
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
]