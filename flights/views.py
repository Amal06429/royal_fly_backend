from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Sum

from .models import Flight, Enquiry
from .serializers import FlightSerializer, EnquirySerializer


# ============================================
# ENQUIRY VIEWS
# ============================================

@api_view(['POST'])
def create_enquiry(request):
    """Create a new enquiry"""
    serializer = EnquirySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Enquiry submitted successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['GET'])
def enquiry_list(request):
    """Get all enquiries"""
    try:
        enquiries = Enquiry.objects.all().order_by('-created_at')
        serializer = EnquirySerializer(enquiries, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# FLIGHT VIEWS
# ============================================

@api_view(['GET', 'POST'])
def flights_api(request):
    """Get all flights or create a new flight"""
    
    if request.method == 'GET':
        try:
            flights = Flight.objects.all().order_by('-created_at')
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            serializer = FlightSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Flight added successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_flight(request, pk):
    """Update a flight"""
    try:
        flight = Flight.objects.get(id=pk)
        serializer = FlightSerializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Flight updated successfully",
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Flight.DoesNotExist:
        return Response({
            "error": "Flight not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_flight(request, pk):
    """Delete a flight"""
    try:
        flight = Flight.objects.get(id=pk)
        flight.delete()
        return Response({
            "message": "Flight deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    except Flight.DoesNotExist:
        return Response({
            "error": "Flight not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================
# DASHBOARD VIEW
# ============================================

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class DashboardAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            total_flights = Flight.objects.count()

            total_seats = Flight.objects.aggregate(
                total=Sum('seat_available')
            )['total'] or 0

            total_enquiries = Enquiry.objects.count()

            today = timezone.now().date()
            today_enquiries = Enquiry.objects.filter(
                created_at__date=today
            ).count()

            recent_enquiries_qs = Enquiry.objects.order_by('-created_at')[:5]
            recent_enquiries = EnquirySerializer(
                recent_enquiries_qs, many=True
            ).data

            return Response({
                "totalFlights": total_flights,
                "totalEnquiries": total_enquiries,
                "todayEnquiries": today_enquiries,
                "totalSeats": total_seats,
                "recentEnquiries": recent_enquiries,
                "user": request.user.email
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
