from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apadrinhamento.urls')),  # <- Aqui você "chama" o urls.py do app
]
