from django.db import models

# Importar todos los modelos
from core.models.categoria import Categoria, Subcategoria
from core.models.pedidos import Pedido, DetallePedido, PedidoProducto
from core.models.configuracion import ConfiguracionGlobal
from core.models.notificaciones import NotificacionProblema, NotificacionReporte
from core.models.mensajes import MensajeContacto
from core.models.usuarios import Usuario
from core.models.rol import Rol
from core.models.repartidores import Repartidor
from core.models.productos import Producto
from core.models.perfil import Profile
from core.models.movimientos import MovimientoProducto
from core.models.lotes import LoteProducto, MovimientoLote
from core.models.imagenes import ImagenProducto, ImagenCategoria
from core.models.distribuidores import Distribuidor, DistribuidorProducto
from core.models.correos_pendientes import CorreoPendiente
from core.models.confirmacion_entrega import ConfirmacionEntrega
from core.models.clientes import Cliente
