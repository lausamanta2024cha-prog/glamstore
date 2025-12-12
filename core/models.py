

from django.db import models

# Create your models here.
from core.models.categoria import Categoria
from core.models.pedidos import Pedido, DetallePedido, PedidoProducto
from core.models.configuracion import ConfiguracionGlobal
from core.models.notificaciones import NotificacionProblema, NotificacionReporte
from core.models.mensajes import MensajeContacto
