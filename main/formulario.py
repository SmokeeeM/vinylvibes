from django import forms
import re

# # Diccionario de regiones y comunas (simplificado para el ejemplo)
REGIONES_COMUNAS = {
    
    "Región de Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Región de Tarapacá": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
    "Región Metropolitana de Santiago": ["Santiago", "Cerrillos", "Ñuñoa", "Vitacura"],
}

# # Generar listas para los choices de las regiones y comunas
REGION_CHOICES = [(region, region) for region in REGIONES_COMUNAS.keys()]
COMUNA_CHOICES = [(comuna, comuna) for region in REGIONES_COMUNAS.values() for comuna in region]

# # class ClienteForm(forms.Form):
# #     nombre = forms.CharField(label="Nombre", max_length=15, required=True)
# #     apellido = forms.CharField(label="Apellido", max_length=20, required=True)
# #     rut = forms.CharField(label="RUT", max_length=12, required=True)
# #     correo = forms.EmailField(label="Correo Electrónico", required=True)
# #     telefono = forms.RegexField(
# #         label="Teléfono",
# #         regex=r'^\d+$',  # Permite solo dígitos
# #         max_length=11,
# #         required=True,
# #         error_messages={'invalido': "Ingrese solo números en este campo."}
# #     )
# #     region = forms.ChoiceField(label="Región", choices=REGION_CHOICES, required=True)
# #     comuna = forms.ChoiceField(label="Comuna", choices=COMUNA_CHOICES, required=True)
# #     direccion = forms.CharField(label="Dirección", max_length=30, required=True)


REGIONES_COMUNAS = {
    "Región de Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Región de Tarapacá": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
    "Región de Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama"],
    "Región de Atacama": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Huasco", "Freirina", "Alto del Carmen"],
    "Región de Coquimbo": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña", "Ovalle", "Monte Patria", "Combarbalá", "Punitaqui", "Río Hurtado"],
    "Región de Valparaíso": ["Valparaíso", "Viña del Mar", "Concón", "Quintero", "Puchuncaví", "Casablanca", "Juan Fernández", "San Antonio", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo", "Quilpué", "Villa Alemana", "Limache", "Olmué"],
    "Región Metropolitana de Santiago": ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil"],
    "Región de O'Higgins": ["Rancagua", "Machalí", "Graneros", "San Francisco de Mostazal", "Rengo", "Requínoa", "Peumo", "Pichidegua", "Las Cabras", "San Vicente", "Pichilemu", "Marchigüe", "Navidad", "Litueche", "La Estrella", "San Fernando", "Santa Cruz", "Chimbarongo", "Nancagua", "Placilla", "Paredones"],
    "Región del Maule": ["Talca", "Curicó", "Linares", "Cauquenes", "Constitución", "Molina", "Parral", "San Clemente", "San Javier", "Teno", "Romeral", "Longaví", "Retiro", "Hualañé", "Licantén", "Vichuquén", "Chanco", "Pelluhue"],
    "Región de Ñuble": ["Chillán", "Bulnes", "Cobquecura", "Coelemu", "El Carmen", "Ninhue", "Pemuco", "Pinto", "Quillón", "Quirihue", "Ránquil", "San Carlos", "San Fabián", "San Ignacio", "San Nicolás", "Treguaco", "Yungay"],
    "Región del Biobío": ["Concepción", "Coronel", "Chiguayante", "Hualpén", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Cabrero", "Laja", "Los Ángeles", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel"],
    "Región de La Araucanía": ["Temuco", "Angol", "Carahue", "Cholchol", "Collipulli", "Cunco", "Curacautín", "Curarrehue", "Ercilla", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Lonquimay", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Purén", "Renaico", "Saavedra", "Teodoro Schmidt", "Toltén", "Traiguén", "Victoria", "Vilcún", "Villarrica"],
    "Región de Los Ríos": ["Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli", "Río Bueno", "La Unión", "Futrono", "Lago Ranco"],
    "Región de Los Lagos": ["Puerto Montt", "Puerto Varas", "Calbuco", "Fresia", "Frutillar", "Llanquihue", "Los Muermos", "Maullín", "Ancud", "Castro", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao", "Chaitén", "Futaleufú", "Hualaihué", "Palena"],
    "Región de Aysén": ["Coyhaique", "Aysén", "Cisnes", "Guaitecas", "Chile Chico", "Río Ibáñez", "Cochrane", "O'Higgins", "Tortel"],
    "Región de Magallanes": ["Punta Arenas", "Puerto Natales", "Porvenir", "Primavera", "Timaukel", "Cabo de Hornos", "Antártica"],
}


REGIONES_COMUNAS = {
    "Región de Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Región de Tarapacá": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
    "Región Metropolitana de Santiago": ["Santiago", "Cerrillos", "Ñuñoa", "Vitacura"],
}


TODAS_COMUNAS = [comuna for comunas in REGIONES_COMUNAS.values() for comuna in comunas]


class ClienteForm(forms.Form):
    rut = forms.CharField(
        max_length=10,
        label="RUT",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 12345678-9'}),
    )
    nombre = forms.CharField(
        max_length=15,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    apellido = forms.CharField(
        max_length=20,
        label="Apellido",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    telefono = forms.RegexField(
    regex=r'^\d{9}$',  # Cambiado para permitir solo 9 dígitos
    label="Número",
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ejemplo: 912345678',  # Sin el símbolo "+"
        'type': 'tel',  # Define que es un campo telefónico
    }),
    error_messages={
        "invalid": "El número debe tener exactamente 9 dígitos sin espacios ni caracteres adicionales. No incluyas el código de área"
    },
    )
    region = forms.ChoiceField(
        label="Región",
        choices=REGION_CHOICES, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    comuna = forms.ChoiceField(
        label="Comuna",
        choices=COMUNA_CHOICES, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    direccion = forms.CharField(
        max_length=30,
        label="Dirección",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if not re.match(r'^\d{7,8}-[\dkK]$', rut):
            raise forms.ValidationError("El RUT debe ser válido (ejemplo: 12345678-9).")
        return rut
