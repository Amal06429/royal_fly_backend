import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Delete all existing users
User.objects.all().delete()
print("Deleted all users.")

# Create fresh superuser with known credentials
user = User.objects.create_superuser(
    username='royalfyadmin',
    email='royalflyadmin@gmail.com',
    password='royalfly123'
)

print(f"\nCreated superuser:")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Password: royalfly123")
print(f"\nYou can now login with these credentials!")
