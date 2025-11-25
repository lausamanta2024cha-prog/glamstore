from django.urls import path
from . import views
from .views import distribuidor_editar_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard principal
     path('', views.index, name='index'),
    path('dashboard/admin/', views.dashboard_admin_view, name='dashboard_admin'),

    # API
    path('api/subcategorias/<int:categoria_id>/', views.api_subcategorias_view, name='api_subcategorias'),

    # Paneles específicos
    path('admin/productos/', views.admin_productos_view, name='admin_productos'),
    path('admin/pedidos/', views.admin_pedidos_view, name='admin_pedidos'),
    path('admin/usuarios/', views.admin_usuarios_view, name='admin_usuarios'),
    path('admin/distribuidores/', views.admin_distribuidores_view, name='admin_distribuidores'),
    path('admin/repartidores/', views.admin_repartidores_view, name='admin_repartidores'),
    path('admin/detalles/', views.admin_detalles_view, name='admin_detalles'),

    # Panel Cliente
    path("clientes/", views.lista_clientes_view, name="lista_clientes"),
    path("clientes/detalle/<int:id>/", views.cliente_detalle_view, name="cliente_detalle"),
    path("clientes/editar/<int:id>/", views.cliente_editar_view, name="cliente_editar"),
    path("clientes/eliminar/<int:id>/", views.cliente_eliminar_view, name="cliente_eliminar"),

    # Panel Distribuidores
    path("distribuidores/", views.lista_distribuidores_view, name="lista_distribuidores"),
    path("distribuidores/agregar/", views.distribuidor_agregar_view, name="agregar_distribuidor"),
    path("distribuidores/editar/<int:id>/", views.distribuidor_editar_view, name="editar_distribuidor"),
    path("distribuidores/eliminar/<int:id>/", views.distribuidor_eliminar_view, name="eliminar_distribuidor"),

    # Panel Reabastecimiento
    path("reabastecimiento/", views.reabastecimiento_view, name="reabastecimiento"),

    # Panel Productos
    path("productos/", views.lista_productos_view, name="lista_productos"),
    path("productos/agregar/", views.producto_agregar_view, name="producto_agregar"),
    path("productos/editar/<int:id>/", views.producto_editar_view, name="producto_editar"),
    path("productos/detalle/<int:id>/", views.producto_detalle_view, name="producto_detalle"),
    path("productos/eliminar/<int:id>/", views.producto_eliminar_view, name="producto_eliminar"),
    path("productos/movimientos/<int:id>/", views.movimientos_producto_view, name="movimientos_producto"),
    path("productos/ajustar_stock/<int:id>/", views.ajustar_stock_view, name="ajustar_stock"),


    # Panel Pedidos
    path('dashboard/admin/pedidos/', views.lista_pedidos_view, name='lista_pedidos'),
    path('dashboard/admin/pedidos/agregar/', views.pedido_agregar_view, name='agregar_pedido'),
    path('dashboard/admin/pedidos/editar/<int:id>/', views.pedido_editar_view, name='editar_pedido'),
    path('dashboard/admin/pedidos/detalle/<int:id>/', views.pedido_detalle_view, name='detalle_pedido'),
    path('dashboard/admin/pedidos/eliminar/<int:id>/', views.pedido_eliminar_view, name='eliminar_pedido'),
    # Panel Repartidores
    path('repartidores/', views.lista_repartidores_view, name='lista_repartidores'),
    path('repartidores/agregar/', views.repartidor_agregar_view, name='repartidor_agregar'),
    path('repartidores/editar/<int:id>/', views.repartidor_editar_view, name='repartidor_editar'),
    path('repartidores/eliminar/<int:id>/', views.repartidor_eliminar_view, name='repartidor_eliminar'),
    path('repartidores/asignar_pedido/', views.asignar_pedido_repartidor_view, name='asignar_pedido_repartidor'),
    path('repartidores/asignar_multiples/', views.asignar_pedidos_multiples_view, name='asignar_pedidos_multiples'),
    path('repartidores/desasignar_multiples/', views.desasignar_pedidos_multiples_view, name='desasignar_pedidos_multiples'),
    path('repartidores/desasignar_pedido/<int:id_pedido>/', views.desasignar_repartidor_view, name='desasignar_repartidor'),
    path('repartidores/descargar_pdf_asignacion/<int:id_pedido>/', views.descargar_pdf_asignacion_view, name='descargar_pdf_asignacion'),
    path('pedidos/descargar_pdf/<int:id_pedido>/', views.descargar_pedido_pdf_view, name='descargar_pedido_pdf'),

    # Panel Admin (perfil)
    path('admin/', views.lista_admin_view, name='lista_admin'), # Esta es la lista principal de administradores
    path('admin/agregar/', views.admin_agregar_view, name='admin_agregar'),
    path('admin/detalle/<int:id>/', views.admin_detalle_view, name='admin_detalle'),
    path('admin/eliminar/<int:id>/', views.admin_eliminar_view, name='admin_eliminar'),
    path('logout/', views.logout_view, name='logout'), # Usamos tu vista personalizada y la nombramos 'logout'

    # Panel Categorías y Subcategorías
    path('categorias/', views.lista_categorias_view, name='lista_categorias'),
    path('categorias/agregar/', views.categoria_agregar_view, name='categoria_agregar'),
    path('categorias/editar/<int:id>/', views.categoria_editar_view, name='categoria_editar'),
    path('categorias/eliminar/<int:id>/', views.categoria_eliminar_view, name='categoria_eliminar'),
    path('subcategorias/', views.lista_subcategorias_view, name='lista_subcategorias'),
    path('subcategorias/agregar/', views.subcategoria_agregar_view, name='subcategoria_agregar'),
    path('subcategorias/editar/<int:id>/', views.subcategoria_editar_view, name='subcategoria_editar'),
    path('subcategorias/eliminar/<int:id>/', views.subcategoria_eliminar_view, name='subcategoria_eliminar'),

    # Notificaciones
    path('notificaciones/', views.notificaciones_view, name='notificaciones'),
    path('notificaciones/marcar_leida/<int:id_notificacion>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones/responder/<int:id_notificacion>/', views.responder_notificacion_view, name='responder_notificacion'),

    # Nuevas funciones de asignación automática y envío de PDFs
    path('repartidores/asignar_automaticamente/', views.asignar_pedidos_automaticamente_view, name='asignar_pedidos_automaticamente'),
    path('repartidores/enviar_pdfs/', views.enviar_pdfs_repartidores_view, name='enviar_pdfs_repartidores'),
    path('repartidores/enviar_correos_seleccionados/', views.enviar_correos_repartidores_seleccionados_view, name='enviar_correos_repartidores_seleccionados'),
    path('repartidores/verificar_capacidad/', views.verificar_capacidad_repartidores_view, name='verificar_capacidad_repartidores'),
    path('repartidores/descargar_pdf/<int:repartidor_id>/', views.descargar_pdf_repartidor_view, name='descargar_pdf_repartidor'),

]
  