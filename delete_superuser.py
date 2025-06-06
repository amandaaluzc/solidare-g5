import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solidare.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
deleted, _ = User.objects.filter(is_superuser=True).delete()

print(f'{deleted} superusuário(s) foram deletados.')