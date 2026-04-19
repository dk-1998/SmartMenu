import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Jelo, Sastojak
from openai import OpenAI
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def lista_jela(request):
    jela = Jelo.objects.all()
    return render(request, 'smart_menu_app/lista_jela.html', {
        'jela': jela
    })
    
@login_required
def dodaj_jelo(request):
    sastojci = Sastojak.objects.all()
    
    if request.method == 'POST' and 'dodaj_jelo' in request.POST:
        naziv_jela = request.POST.get('naziv_jela')
        opis = request.POST.get('opis')
        kategorija = request.POST.get('kategorija')
        cena = request.POST.get('cena')
        dostupno = True if request.POST.get('dostupno') == 'on' else False
        izabrani_sastojci_ids = request.POST.getlist('sastojci')

        if naziv_jela and opis and kategorija and cena:
            novo_jelo = Jelo.objects.create(
                naziv_jela=naziv_jela,
                opis=opis,
                kategorija=kategorija,
                cena=cena,
                dostupno=dostupno
            )
            if izabrani_sastojci_ids:
                novo_jelo.sastojci.set(izabrani_sastojci_ids)
            novo_jelo.save()
            messages.success(request, f"Jelo '{novo_jelo.naziv_jela}' uspešno dodato!")
            return redirect('dodaj_jelo')
        else:
            messages.error(request, "Molimo popunite sva polja!")

    return render(request, 'smart_menu_app/dodaj_jelo.html', {
        'sastojci': sastojci
    })
    

    
@login_required
def ai(request):
    jela = Jelo.objects.all()
    odgovori = {}
    
    if request.method == 'POST' and 'postavi_pitanje' in request.POST:
        pitanje = request.POST.get('pitanje')
        izabrana_jela_ids = request.POST.getlist('jela')

        if pitanje and izabrana_jela_ids:
            api_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")
            if not api_key:
                messages.error(request, "OpenAI API ključ nije postavljen.")
            else:
                client = OpenAI(api_key=api_key)

                for jelo_id in izabrana_jela_ids:
                    try:
                        jelo = Jelo.objects.get(id=jelo_id)
                        sastojci_jela = ", ".join([s.naziv_sastojka for s in jelo.sastojci.all()])

                        prompt = (
                            f"Pitanje: {pitanje}\n"
                            f"Jelo: {jelo.naziv_jela}\n"
                            f"Opis: {jelo.opis}\n"
                            f"Cena: {jelo.cena} RSD\n"
                            f"Dostupno: {'Da' if jelo.dostupno else 'Ne'}\n"
                            f"Sastojci: {sastojci_jela}\n"
                            "Odgovori detaljno i iscrpno:"
                        )

                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "Ti si stručni AI asistent za hranu i jela. Odgovaraj detaljno i iscrpno."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.7,
                            max_tokens=1000
                        )

                        odgovor = response.choices[0].message.content.strip()

                    except Exception as e:
                        odgovor = f"Greška pri dobijanju odgovora: {str(e)}"

                    odgovori[jelo.naziv_jela] = odgovor
        else:
            messages.error(request, "Odaberite barem jedno jelo i postavite pitanje.")

    return render(request, 'smart_menu_app/ai.html', {
        'jela': jela,
        'odgovori': odgovori
    })



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Lozinke se ne poklapaju!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Korisničko ime već postoji!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Uspešno ste se registrovali! Možete se prijaviti.")
        return redirect('login')

    return render(request, 'smart_menu_app/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dodaj_jelo')  # Redirekt na dodavanje jela posle logina
        else:
            messages.error(request, "Neispravno korisničko ime ili lozinka!")
            return redirect('login')
    return render(request, 'smart_menu_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def logout_ajax(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)