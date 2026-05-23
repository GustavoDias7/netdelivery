from django.core.management.base import BaseCommand
from django.conf import settings
from apps.user.models import User
from environs import Env
from django.db import IntegrityError

env = Env()
env.read_env() 

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(
                email=env("DJANGO_SUPERUSER_EMAIL"),
                username=env("DJANGO_SUPERUSER_USERNAME"),
                password=env("DJANGO_SUPERUSER_PASSWORD")
            )
        except IntegrityError as e:
            print(e)

