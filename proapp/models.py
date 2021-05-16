from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Konyv(models.Model):
    cim = models.CharField(max_length=100)
    iro = models.CharField(max_length=100)
    leiras = models.TextField(blank=True, null=True)
    ar = models.IntegerField()
    elerheto = models.BooleanField(default=True)
    fajlnev = models.CharField(max_length=40, default='biblia.jpeg')

    def __str__(self):
        return "{} {} ({})".format(self.iro, self.cim, self.pk)

    def get_absolute_url(self):
        return reverse('proapp:konyvhozzaadas')

class OlvasoEst(models.Model):
    elnevezes = models.CharField(max_length=100)
    idopont = models.DateTimeField()
    helyekszama = models.IntegerField(default=20)

    def __str__(self):
        return "{} {} ({})".format(self.elnevezes, self.idopont, self.pk)

class Kolcsonzes(models.Model):
    felhasznalo = models.ForeignKey(User, on_delete=models.CASCADE)
    konyv = models.ForeignKey(Konyv, on_delete=models.CASCADE)
    kezdet = models.DateTimeField(default=timezone.now)
    veg = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format(self.felhasznalo.username, self.konyv.cim, self.kezdet.strftime('%Y-%m-%d'))

class Resztvetel(models.Model):
    felhasznalo = models.ForeignKey(User, on_delete=models.CASCADE)
    olvasoest = models.ForeignKey(OlvasoEst, on_delete=models.CASCADE)
    fizetve = models.BooleanField(default=False)
    idopont = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {}".format(self.felhasznalo.username, self.olvasoest.elnevezes)
