from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from .models import Producto
from .formulario import *
from transbank.webpay.webpay_plus.transaction import Transaction
from cryptography.fernet import Fernet, InvalidToken
import re
import json

#vista inicial, en donde se muestra la pagina principal y los productos
def index(request):
    productos = Producto.objects.all()
    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(nombre__icontains=query)
    return render(request, 'index.html', {'productos': productos, 'query': query})


def detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle.html', {'producto': producto})




# def agregar_al_carrito(request, producto_id):
#     producto = get_object_or_404(Producto, id=producto_id)
#     carrito = request.session.get('carrito', {})

#     if str(producto_id) in carrito:
#         carrito[str(producto_id)]['cantidad'] += 1
#     else:
#         carrito[str(producto_id)] = {
#             'nombre': producto.nombre,
#             'precio': str(producto.precio),
#             'imagen': producto.imagen.url,
#             'cantidad': 1,
#         }

#     request.session['carrito'] = carrito
#     return redirect('index')  # Cambia 'ver_carrito' por el nombre de tu vista


def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad <= 0:
                messages.error(request, "La cantidad debe ser mayor que cero.")
                return redirect('detalle', producto_id=producto.id)

            # Cantidad ya en el carrito
            cantidad_actual_en_carrito = carrito.get(str(producto.id), {}).get('cantidad', 0)
            
            # Verificar el stock disponible considerando el carrito
            if cantidad + cantidad_actual_en_carrito > producto.stock:
                messages.error(
                    request,
                    f"No hay suficiente stock disponible. Máximo permitido: {producto.stock - cantidad_actual_en_carrito} unidades."
                )
                return redirect('detalle', producto_id=producto.id)
        except ValueError:
            messages.error(request, "Cantidad no válida.")
            return redirect('detalle', producto_id=producto.id)

        if str(producto.id) in carrito:
            carrito[str(producto.id)]['cantidad'] += cantidad
        else:
            carrito[str(producto.id)] = {
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': str(producto.precio),
                'imagen': producto.imagen.url if producto.imagen else ''
            }

        request.session['carrito'] = carrito
        messages.success(request, f'{producto.nombre} ha sido agregado al carrito.')
        return redirect('detalle', producto_id=producto.id)

    return render(request, 'index', {'producto': producto})





def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})


def vaciar_carrito(request):
    if 'carrito' in request.session:
            request.session['carrito'] = {}

    return redirect('ver_carrito')  


def eliminar_producto(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    # Verifica si el producto está en el carrito
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito  # Actualiza el carrito en la sesión
    
    return redirect('ver_carrito')  # Cambia por el nombre de tu vista de carrito si es distinto

from django.shortcuts import render, redirect


# Validación de formato de RUT
def is_valid_rut(rut):
    pattern = r"^\d{7,8}-[0-9Kk]$"
    return re.match(pattern, rut) is not None

# views.py
from django.shortcuts import render, redirect
from .formulario import ClienteForm
from transbank.webpay.webpay_plus.transaction import Transaction
import uuid

def checkout(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Guardar datos del cliente en la sesión
            request.session['cliente'] = form.cleaned_data

            # Calcular el total del carrito
            carrito = request.session.get("carrito", {})
            total = round(sum(float(item['precio']) * int(item['cantidad']) for item in carrito.values()), 3)

            # Crear la transacción con WebPay

            orden_de_compra = f"orden-{uuid.uuid4().hex[:8]}" 
            sesion = request.session.session_key
            url_retorno = request.build_absolute_uri('/resultado_pago/')  # URL de confirmación

            transaction = Transaction().create(
                buy_order= orden_de_compra,
                session_id= sesion,
                amount=total,
                return_url= url_retorno
            )

            # Redirigir a WebPay
            return redirect(transaction['url'] + "?token_ws=" + transaction['token'])

    else:
        form = ClienteForm()

    # Mostrar el formulario si no es un POST
    carrito = request.session.get("carrito", {})
    total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito.values())
    return render(request, 'checkout.html', {
        'form': form,
        'carrito': carrito,
        'total': total,
    })

from transbank.webpay.webpay_plus.transaction import Transaction
from django.shortcuts import get_object_or_404

def resultado_pago(request):
    # Revisar si el token viene por POST o GET
    token = request.POST.get('token_ws') or request.GET.get('token_ws')

    if not token:
        return render(request, 'error.html', {'mensaje': 'No se recibió el token del pago.'})

    try:
        # Procesar la transacción
        response = Transaction().commit(token)

        if response['status'] == 'AUTHORIZED':
            # Obtener el carrito de la sesión
            carrito = request.session.get('carrito', {})

            # Actualizar el stock de cada producto en el carrito
            for product_id, item in carrito.items():
                producto = get_object_or_404(Producto, id=product_id)
                cantidad_comprada = int(item['cantidad'])
                
                # Validar stock disponible
                if producto.stock < cantidad_comprada:
                    return render(request, 'error.html', {'mensaje': f"El producto {producto.nombre} no tiene suficiente stock."})

                # Restar el stock
                producto.stock -= cantidad_comprada
                producto.save()

            # Vaciar el carrito tras la compra
            request.session['carrito'] = {}

            # Renderizar la página de éxito
            return render(request, 'pago_exitoso.html', {'response': response})

        return render(request, 'error.html', {'mensaje': 'El pago no fue autorizado.'})

    except Exception as e:
        return render(request, 'error.html', {'mensaje': f'Ocurrió un error al procesar el pago: {str(e)}'})



