from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detalle, name='detalle'),
    path('agregar_carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('checkout/', views.checkout, name='checkout'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),




]