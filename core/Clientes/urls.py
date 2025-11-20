from django.urls import path
from django.contrib.auth import views as auth_views
from core.Clientes import views



urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('tienda/', views.tienda, name='tienda'),
    path('carrito/', views.carrito, name='ver_carrito'),
    path('perfil/', views.perfil, name='perfil'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('categoria/<int:id_categoria>/', views.productos_por_categoria, name='productos_categoria'),
    path('subcategoria/<str:nombreSubcategoria>/', views.productos_por_subcategoria, name='productos_subcategoria'),
    path('debug-carrito/', views.ver_carrito_debug, name='ver_carrito_debug'),
    path('eliminar-del-carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-cantidad-carrito/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('simular-pago/', views.simular_pago, name='simular_pago'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('cambiar-password/<str:token>/', views.cambiar_password, name='cambiar_password'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('contacto/', views.contacto, name='contacto'),
    path('crear-usuario-desde-cliente/', views.crear_usuario_desde_cliente, name='crear_usuario_desde_cliente'),
    path('pedido_confirmado/<int:idPedido>/', views.pedido_confirmado, name='pedido_confirmado'),
    path('ver_seguimiento/<int:idPedido>/', views.ver_seguimiento, name='ver_seguimiento'),
]