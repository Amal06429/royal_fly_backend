from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import UserProfile


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_staff
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """Refresh the access token using refresh token"""
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class UsersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List users created by the current admin"""
        if not request.user.is_staff:
            return Response(
                {"error": "Only admins can view users"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Backfill missing profiles for legacy deployment users.
        try:
            legacy_users = User.objects.filter(is_staff=False, userprofile__isnull=True)
            for legacy_user in legacy_users:
                UserProfile.objects.get_or_create(
                    user=legacy_user,
                    defaults={
                        'created_by': None,
                        'password_display': ''
                    }
                )

            # Show users created by current admin + legacy users without ownership.
            user_profiles = UserProfile.objects.filter(
                Q(created_by=request.user) | Q(created_by__isnull=True),
                user__is_staff=False
            ).select_related('user').order_by('-user__date_joined')
            
            users_data = []
            for profile in user_profiles:
                users_data.append({
                    'id': profile.user.id,
                    'username': profile.user.username,
                    'email': profile.user.email,
                    'password': profile.password_display
                })
            
            return Response(users_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Error loading users: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Create a new user - Admin only"""
        if not request.user.is_staff:
            return Response(
                {"error": "Only admins can create users"},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response(
                {"error": "username, email, and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=False
            )

            # Ensure profile is always present for newly created users.
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'created_by': request.user,
                    'password_display': password
                }
            )

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": password
        }, status=status.HTTP_201_CREATED)


class UserDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        """Delete a user - Admin only"""
        try:
            if not request.user.is_staff:
                return Response(
                    {"error": "Only admins can delete users"},
                    status=status.HTTP_403_FORBIDDEN
                )

            if not user_id:
                return Response(
                    {"error": "user_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Prevent deleting yourself
            if request.user.id == int(user_id):
                return Response(
                    {"error": "Cannot delete your own account"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.get(id=user_id)
            
            # Check if current admin created this user
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.created_by and profile.created_by != request.user:
                    return Response(
                        {"error": "You can only delete users you created"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            username = user.username
            user.delete()
            
            return Response(
                {"message": f"User {username} deleted successfully"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error deleting user: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )