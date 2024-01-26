from django.db import models


# Create your models here.
class SiteParameters(models.Model):
    orphanage_name = models.CharField(max_length=100, verbose_name="Nom de l'orphelinat",  blank=True)
    address = models.TextField(verbose_name="Adresse de l'orphelinat", blank=True)
    phone_number = models.CharField(max_length=15, verbose_name="Numéro de téléphone", blank=True)
    opening_hours = models.CharField(max_length=50, verbose_name="Heures d'ouverture", blank=True)
    about_us = models.TextField(verbose_name="À propos de nous", blank=True)
    homepage_image = models.ImageField(upload_to='homepage_images/', verbose_name="Image d'accueil", blank=True)

    def __str__(self):
        return self.orphanage_name

    class Meta:
        verbose_name_plural = "Paramètres du site"


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Visitor - {self.timestamp}'
