from rest_framework import serializers
from .models import Flight, Enquiry

# ========================================
# ENQUIRY SERIALIZER
# ========================================
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'from_city',
            'to_city',
            'travel_date',
            'notes',
            'message',
            'created_by',
            'created_at'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'travel_date': {'required': False},
            'notes': {'required': False},
            'message': {'required': False},
            'created_by': {'required': False}
        }



# ========================================
# FLIGHT SERIALIZER (CamelCase <-> Snake Case)
# ========================================
class FlightSerializer(serializers.ModelSerializer):

    # Frontend → Backend mapping
    tripType = serializers.CharField(source='trip_type')
    flightType = serializers.CharField(source='flight_type')

    departureCode = serializers.CharField(source='departure_code')
    departureCity = serializers.CharField(source='departure_city')

    destinationCode = serializers.CharField(source='destination_code')
    destinationCity = serializers.CharField(source='destination_city')

    departureDate = serializers.DateField(source='departure_date')
    departureTime = serializers.TimeField(source='departure_time')

    returnDate = serializers.DateField(
        source='return_date', required=False, allow_null=True
    )
    returnTime = serializers.TimeField(
        source='return_time', required=False, allow_null=True
    )

    seatAvailable = serializers.IntegerField(source='seat_available')

    class Meta:
        model = Flight
        fields = [
            'id',
            'tripType',
            'flightType',
            'departureCode',
            'departureCity',
            'destinationCode',
            'destinationCity',
            'departureDate',
            'departureTime',
            'returnDate',
            'returnTime',
            'airline',
            'price',
            'seatAvailable'
        ]
