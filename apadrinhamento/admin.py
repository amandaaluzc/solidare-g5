from django.contrib import admin
from .models import Crianca, Padrinho, Apadrinhamento

class CriancaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'genero')
    list_filter = ('idade', 'genero') 

admin.site.register(Crianca)
admin.site.register(Padrinho)
admin.site.register(Apadrinhamento)
