from django.contrib import admin
from .models import Jelo, Sastojak

# ---- Sastojak ----
@admin.register(Sastojak)
class SastojakAdmin(admin.ModelAdmin):
    list_display = ('naziv_sastojka', 'alergen', 'tip')  
    list_filter = ('tip', 'alergen')                    
    search_fields = ('naziv_sastojka',)             

# ---- Jelo ----
@admin.register(Jelo)
class JeloAdmin(admin.ModelAdmin):
    list_display = ('naziv_jela', 'kategorija', 'cena', 'dostupno') 
    list_filter = ('kategorija', 'dostupno')                         
    search_fields = ('naziv_jela', 'opis')                             
    filter_horizontal = ('sastojci',)                              
