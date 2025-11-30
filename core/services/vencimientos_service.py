from datetime import date, timedelta
from django.db.models import Q, Sum
from core.models.lotes import LoteProducto
from core.models.productos import Producto


class VencimientosService:
    
    @staticmethod
    def obtener_productos_vencidos():
        """
        Obtiene todos los lotes que ya están vencidos
        """
        hoy = date.today()
        
        lotes_vencidos = LoteProducto.objects.filter(
            fecha_vencimiento__lt=hoy,
            cantidad_disponible__gt=0
        ).select_related('producto').order_by('fecha_vencimiento')
        
        productos_vencidos = []
        for lote in lotes_vencidos:
            productos_vencidos.append({
                'producto': lote.producto,
                'lote': lote,
                'dias_vencido': (hoy - lote.fecha_vencimiento).days,
                'cantidad_perdida': lote.cantidad_disponible,
                'valor_perdido': lote.cantidad_disponible * lote.costo_unitario if lote.costo_unitario else 0
            })
        
        return productos_vencidos
    
    @staticmethod
    def obtener_productos_por_vencer(dias_alerta=30):
        """
        Obtiene productos que están por vencerse en los próximos X días
        """
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=dias_alerta)
        
        lotes_por_vencer = LoteProducto.objects.filter(
            fecha_vencimiento__gte=hoy,
            fecha_vencimiento__lte=fecha_limite,
            cantidad_disponible__gt=0
        ).select_related('producto').order_by('fecha_vencimiento')
        
        productos_por_vencer = []
        for lote in lotes_por_vencer:
            dias_restantes = (lote.fecha_vencimiento - hoy).days
            
            # Determinar nivel de urgencia
            if dias_restantes <= 7:
                urgencia = 'critica'
            elif dias_restantes <= 15:
                urgencia = 'alta'
            else:
                urgencia = 'media'
            
            productos_por_vencer.append({
                'producto': lote.producto,
                'lote': lote,
                'dias_restantes': dias_restantes,
                'fecha_vencimiento': lote.fecha_vencimiento,
                'cantidad_disponible': lote.cantidad_disponible,
                'valor_en_riesgo': lote.cantidad_disponible * lote.costo_unitario if lote.costo_unitario else 0,
                'urgencia': urgencia
            })
        
        return productos_por_vencer
    
    @staticmethod
    def obtener_resumen_vencimientos():
        """
        Obtiene un resumen general de vencimientos
        """
        productos_vencidos = VencimientosService.obtener_productos_vencidos()
        productos_por_vencer = VencimientosService.obtener_productos_por_vencer()
        
        # Calcular totales
        total_productos_vencidos = len(productos_vencidos)
        total_cantidad_vencida = sum(p['cantidad_perdida'] for p in productos_vencidos)
        total_valor_perdido = sum(p['valor_perdido'] for p in productos_vencidos)
        
        total_productos_por_vencer = len(productos_por_vencer)
        total_cantidad_por_vencer = sum(p['cantidad_disponible'] for p in productos_por_vencer)
        total_valor_en_riesgo = sum(p['valor_en_riesgo'] for p in productos_por_vencer)
        
        # Contar por urgencia
        criticos = len([p for p in productos_por_vencer if p['urgencia'] == 'critica'])
        altos = len([p for p in productos_por_vencer if p['urgencia'] == 'alta'])
        medios = len([p for p in productos_por_vencer if p['urgencia'] == 'media'])
        
        return {
            'productos_vencidos': {
                'total_productos': total_productos_vencidos,
                'total_cantidad': total_cantidad_vencida,
                'total_valor': total_valor_perdido,
                'detalle': productos_vencidos[:10]  # Solo los primeros 10 para el dashboard
            },
            'productos_por_vencer': {
                'total_productos': total_productos_por_vencer,
                'total_cantidad': total_cantidad_por_vencer,
                'total_valor': total_valor_en_riesgo,
                'criticos': criticos,
                'altos': altos,
                'medios': medios,
                'detalle': productos_por_vencer[:10]  # Solo los primeros 10 para el dashboard
            }
        }
    
    @staticmethod
    def marcar_lotes_vencidos_como_perdidos():
        """
        Marca los lotes vencidos como perdidos (cantidad_disponible = 0)
        y registra el movimiento de pérdida
        """
        from core.models.movimientos import MovimientoProducto
        
        hoy = date.today()
        lotes_vencidos = LoteProducto.objects.filter(
            fecha_vencimiento__lt=hoy,
            cantidad_disponible__gt=0
        )
        
        movimientos_creados = []
        
        for lote in lotes_vencidos:
            cantidad_perdida = lote.cantidad_disponible
            
            # Crear movimiento de pérdida
            movimiento = MovimientoProducto.objects.create(
                producto=lote.producto,
                tipo_movimiento='PERDIDA_VENCIMIENTO',
                cantidad=cantidad_perdida,
                stock_anterior=lote.producto.stock,
                stock_nuevo=lote.producto.stock - cantidad_perdida,
                descripcion=f'Pérdida por vencimiento - Lote {lote.codigo_lote}',
                lote_origen=lote
            )
            
            # Actualizar stock del producto
            lote.producto.stock -= cantidad_perdida
            lote.producto.cantidadDisponible -= cantidad_perdida
            lote.producto.save()
            
            # Marcar lote como agotado
            lote.cantidad_disponible = 0
            lote.save()
            
            movimientos_creados.append(movimiento)
        
        return movimientos_creados
    
    @staticmethod
    def obtener_productos_sin_fecha_vencimiento():
        """
        Obtiene productos que tienen lotes sin fecha de vencimiento definida
        """
        lotes_sin_fecha = LoteProducto.objects.filter(
            fecha_vencimiento__isnull=True,
            cantidad_disponible__gt=0
        ).select_related('producto')
        
        productos_sin_fecha = []
        for lote in lotes_sin_fecha:
            productos_sin_fecha.append({
                'producto': lote.producto,
                'lote': lote,
                'cantidad_disponible': lote.cantidad_disponible,
                'fecha_entrada': lote.fecha_entrada
            })
        
        return productos_sin_fecha