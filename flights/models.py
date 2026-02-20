from django.db import models

# ========================================
# ENQUIRY MODEL
# ========================================
class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    from_city = models.CharField(max_length=50)
    to_city = models.CharField(max_length=50)
    message = models.TextField(blank=True)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'flight'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.departure_city} ({self.departure_code}) → {self.destination_city} ({self.destination_code})"
 