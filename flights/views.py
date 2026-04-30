from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
        # Save with user if authenticated
        if request.user and request.user.is_authenticated:
            serializer.save(user=request.user)
        else:
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def enquiry_list(request):
    """Get enquiries based on logged-in user's role."""
    try:
        if request.user.is_staff:
            enquiries = Enquiry.objects.all().order_by('-created_at')
        else:
            enquiries = Enquiry.objects.filter(user=request.user).order_by('-created_at')

        serializer = EnquirySerializer(enquiries, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE', 'PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def enquiry_detail(request, pk):
    """Get, update (PATCH/PUT), or delete an enquiry"""
    try:
        enquiry = Enquiry.objects.get(id=pk)

        # Non-admin users can access only their own enquiries.
        if not request.user.is_staff and enquiry.user_id != request.user.id:
            return Response({
                "error": "You can only access your own enquiries"
            }, status=status.HTTP_403_FORBIDDEN)
        
        if request.method == 'DELETE':
            enquiry.delete()
            return Response({
                "message": "Enquiry deleted successfully"
            }, status=status.HTTP_200_OK)
        
        elif request.method in ['PATCH', 'PUT']:
            # For PATCH, use partial=True; for PUT, use partial=False
            partial = request.method == 'PATCH'
            serializer = EnquirySerializer(enquiry, data=request.data, partial=partial)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Enquiry updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Enquiry.DoesNotExist:
        return Response({
            "error": "Enquiry not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_enquiry(request, pk):
    """Delete an enquiry"""
    try:
        enquiry = Enquiry.objects.get(id=pk)

        if not request.user.is_staff and enquiry.user_id != request.user.id:
            return Response({
                "error": "You can only delete your own enquiries"
            }, status=status.HTTP_403_FORBIDDEN)

        enquiry.delete()
        return Response({
            "message": "Enquiry deleted successfully"
        }, status=status.HTTP_200_OK)
    except Enquiry.DoesNotExist:
        return Response({
            "error": "Enquiry not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_enquiry(request, pk):
    """Update an enquiry (partial update with PATCH, full update with PUT)"""
    try:
        enquiry = Enquiry.objects.get(id=pk)

        if not request.user.is_staff and enquiry.user_id != request.user.id:
            return Response({
                "error": "You can only update your own enquiries"
            }, status=status.HTTP_403_FORBIDDEN)
        
        # For PATCH, use partial=True; for PUT, use partial=False
        partial = request.method == 'PATCH'
        serializer = EnquirySerializer(enquiry, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Enquiry updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Enquiry.DoesNotExist:
        return Response({
            "error": "Enquiry not found"
        }, status=status.HTTP_404_NOT_FOUND)
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
            if request.user.is_authenticated and not request.user.is_staff:
                flights = Flight.objects.filter(creator_user=request.user).order_by('-created_at')
            else:
                flights = Flight.objects.all().order_by('-created_at')

            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return Response({
                    "error": "Authentication required"
                }, status=status.HTTP_401_UNAUTHORIZED)

            data = request.data.copy()
            
            # Set created_by and creator_user based on authentication
            if request.user.is_authenticated:
                data['created_by'] = 'admin' if request.user.is_staff else 'user'
                creator_user = request.user
            else:
                data['created_by'] = 'user'
                creator_user = None
            
            serializer = FlightSerializer(data=data)
            if serializer.is_valid():
                flight = serializer.save(creator_user=creator_user)
                return Response({
                    "message": "Flight added successfully",
                    "data": FlightSerializer(flight).data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_flight(request, pk):
    """Update a flight"""
    try:
        flight = Flight.objects.get(id=pk)

        if not request.user.is_staff and flight.creator_user_id != request.user.id:
            return Response({
                "error": "You can only update your own tickets"
            }, status=status.HTTP_403_FORBIDDEN)

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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_flight(request, pk):
    """Delete a flight"""
    try:
        flight = Flight.objects.get(id=pk)

        if not request.user.is_staff and flight.creator_user_id != request.user.id:
            return Response({
                "error": "You can only delete your own tickets"
            }, status=status.HTTP_403_FORBIDDEN)

        flight.delete()
        return Response({
            "message": "Flight deleted successfully"
        }, status=status.HTTP_200_OK)
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

class DashboardAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            flights_qs = Flight.objects.all() if request.user.is_staff else Flight.objects.filter(creator_user=request.user)
            enquiries_qs = Enquiry.objects.all() if request.user.is_staff else Enquiry.objects.filter(user=request.user)

            total_flights = flights_qs.count()

            total_seats = flights_qs.aggregate(
                total=Sum('seat_available')
            )['total'] or 0

            total_enquiries = enquiries_qs.count()

            today = timezone.now().date()
            today_enquiries = enquiries_qs.filter(
                created_at__date=today
            ).count()

            recent_enquiries_qs = enquiries_qs.order_by('-created_at')[:5]
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
