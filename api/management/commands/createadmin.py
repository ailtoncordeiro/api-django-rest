from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from getpass import getpass

class Command(BaseCommand):
    help = 'Create a superuser with a name'

    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('name')
        parser.add_argument('--password', dest='password', help='User password', type=str)

    def handle(self, *args, **options):
        email = options['email']
        name = options['name']
        password = options['password'] or getpass('Password: ')
        User = get_user_model()
        try:
            User.objects.create_superuser(email=email, password=password, name=name)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(str(e)))
