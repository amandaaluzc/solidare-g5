import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solidare.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "adminsolidare"
email = "admin@example.com"
password = "admin123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuário criado com sucesso.")
else:
    print("Superusuário já existe.")