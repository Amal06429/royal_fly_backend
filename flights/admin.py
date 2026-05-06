from django.contrib import admin
from .models import Flight, Enquiry, Visa

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'departure_city', 'destination_city', 'departure_date', 'airline', 'price']
    search_fields = ['departure_city', 'destination_city', 'airline']
    list_filter = ['departure_date', 'airline']

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'from_city', 'to_city', 'status', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['status', 'created_at']

@admin.register(Visa)
class VisaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fill_no', 'passport_number', 'contact_no', 'visa_date', 'user', 'created_at']
    search_fields = ['fill_no', 'passport_number', 'contact_no']
    list_filter = ['visa_date', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
