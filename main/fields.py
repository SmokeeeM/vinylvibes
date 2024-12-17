from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

class EncryptedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.key = settings.LLAVECITA.decode()  # Usa la clave codificada en Base64
        self.fernet = Fernet(self.key)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """Cifra el valor antes de guardarlo"""
        if value:
            value = self.fernet.encrypt(value.encode()).decode()  # Cifra el valor
        return super().get_prep_value(value)

    def from_db_value(self, value, expression, connection):
        """Descifra el valor al obtenerlo de la base de datos"""
        if value:
            try:
                value = self.fernet.decrypt(value.encode()).decode()  # Descifra el valor
            except InvalidToken:
                # Maneja el caso de un token inválido retornando un valor predeterminado
                return "Valor inválido o corrupto"
        return value
