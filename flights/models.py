from django.db import models
from django.contrib.auth.models import User

# ========================================
# ENQUIRY MODEL
# ========================================
class Enquiry(models.Model):
    ENQUIRY_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    from_city = models.CharField(max_length=50)
    to_city = models.CharField(max_length=50)
    travel_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    message = models.TextField(blank=True)  # Keep for backward compatibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    fare_type = models.CharField(max_length=50, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pnr = models.CharField(max_length=50, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    label_name = models.CharField(max_length=500, blank=True, null=True)
    label_colour = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.CharField(max_length=10, choices=ENQUIRY_TYPE_CHOICES, default='customer')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'enquiry'
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'
 
    def __str__(self):
        return f"{self.name} - {self.from_city} → {self.to_city}"


# ========================================
# FLIGHT MODEL
# ========================================
class Flight(models.Model):
    FLIGHT_CREATOR_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    trip_type = models.CharField(max_length=20)
    flight_type = models.CharField(max_length=20)
       
    departure_code = models.CharField(max_length=3)
    departure_city = models.CharField(max_length=50)

    destination_code = models.CharField(max_length=3)
    destination_city = models.CharField(max_length=50)

    departure_date = models.DateField()
    departure_time = models.TimeField()

    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
 
    airline = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seat_available = models.IntegerField()

    created_by = models.CharField(max_length=10, choices=FLIGHT_CREATOR_CHOICES, default='user')
    creator_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_flights')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flight'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.departure_city} ({self.departure_code}) → {self.destination_city} ({self.destination_code})"
 