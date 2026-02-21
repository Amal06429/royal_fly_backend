import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# List all users
print("\n=== ALL USERS ===")
users = User.objects.all()
for u in users:
    print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")

# Delete all users except the most recent one
print("\n=== CLEANING UP ===")
if users.count() > 1:
    latest_user = users.order_by('-id').first()
    print(f"Keeping latest user: ID={latest_user.id}, Username={latest_user.username}, Email={latest_user.email}")
    
    # Delete all users except the latest
    User.objects.exclude(id=latest_user.id).delete()
    print("Deleted old duplicate users.")
else:
    print("Only one user found. No cleanup needed.")

print("\n=== REMAINING USERS ===")
users = User.objects.all()
for u in users:
    print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")
