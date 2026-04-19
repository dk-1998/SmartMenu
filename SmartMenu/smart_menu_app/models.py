from django.db import models

class Sastojak(models.Model):
    naziv_sastojka = models.CharField(max_length=255)
    alergen = models.BooleanField(default=False)
    tip = models.CharField(max_length=50)

    def __str__(self):
        return self.naziv_sastojka


class Jelo(models.Model):
    naziv_jela = models.CharField(max_length=255)
    opis = models.TextField()
    kategorija = models.CharField(max_length=50)
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    dostupno = models.BooleanField(default=True)
    sastojci = models.ManyToManyField(Sastojak, related_name="jela")  # ← OVO je ključno

    def __str__(self):
        return self.naziv_jela
