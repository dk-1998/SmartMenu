from django.urls import path
from . import views

urlpatterns = [
    path('dodaj_jelo/', views.dodaj_jelo, name='dodaj_jelo'),
    path('lista_jela/', views.lista_jela, name='lista_jela'),
    path('ai/', views.ai, name='ai'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout_ajax/', views.logout_ajax, name='logout_ajax'),  # Dodaj ovu liniju
]