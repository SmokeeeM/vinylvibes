from django.db import models
from django.core.exceptions import ValidationError
from .fields import *  # Importar los campos personalizados

class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    descripcion = EncryptedCharField(max_length=200)  # Usamos EncryptedTextField para la descripción
    precio = models.DecimalField(max_digits=10, decimal_places=3)
    imagen = models.ImageField(upload_to='productos/', null=False, blank=False)
    stock = models.PositiveIntegerField()
    artista = EncryptedCharField(max_length=45)  # Usamos EncryptedCharField para el artista


# class Producto(models.Model):
#     nombre = models.CharField(max_length=45)
#     descripcion = models.TextField()
#     precio = models.DecimalField(max_digits=6, decimal_places=3)
#     imagen = models.ImageField(upload_to='productos/', null=False, blank=False)
#     stock = models.PositiveIntegerField()
#     artista = models.CharField(max_length=45)



    def __str__(self):
        return self.nombre

    def tiene_stock(self):
        return self.stock > 0
    
