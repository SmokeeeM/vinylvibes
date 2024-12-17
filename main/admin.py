from django.contrib import admin
from .models import Producto
# admin / fuckyou321
# debito: 5186059559590564
#user 11.111.111-1 / 123

admin.site.register(Producto)
#para poder administrar mi modelo producto, debo primero registrarlo dentro de la administración del sitio
#si no registro acá los modelos que quiero administrar, no aprecerán en el panel de administración
