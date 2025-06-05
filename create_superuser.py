#!/usr/bin/env python
import os
import django

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'solidare.settings_test':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solidare.settings_test')
    django.setup()

    from django.contrib.auth.models import User

    username = 'Solidareadmin'
    email = 'admin@solidare.com'
    password = 'ADM12345'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superusuário {username} criado com sucesso.')
    else:
        print(f'Superusuário {username} já existe.')
else:
    print("Não está no ambiente de teste, superusuário não será criado.")
