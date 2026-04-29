from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from login.models import UserProfile


class Command(BaseCommand):
    help = 'Initialize UserProfile for existing users without profiles'

    def handle(self, *args, **options):
        # Get all users
        users = User.objects.all()
        
        for user in users:
            # Create profile if it doesn't exist
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'created_by': None,  # None for existing users (not admin-created)
                    'password_display': ''  # Empty password for existing users
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for user: {user.username}')
                )
            else:
                self.stdout.write(f'Profile already exists for user: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS('User profiles initialization completed!')
        )
