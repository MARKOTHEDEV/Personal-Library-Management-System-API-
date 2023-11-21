"""
command for the application to Admin
"""
from django.core.management import BaseCommand
from authentication.models import User
import os



class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_mail = os.environ['admin_mail']
        admin_password = os.environ['admin_password']
        if not User.objects.filter(email=admin_mail).exists():
            super_admin = User.objects.create_superuser(
                email=admin_mail,
                password=admin_password
            )
            self.stdout.write('Create Super Successfully!')
        else:
            self.stdout.write('Hey man this admin is created already check env for info!')

