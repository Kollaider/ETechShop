from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clear all tables except for the admin entities'

    def handle(self, *args, **options):
        # Call flush command to reset the database
        call_command('flush', interactive=False)

        self.stdout.write(self.style.SUCCESS('Database cleared successfully'))