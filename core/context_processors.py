"""
Context processors para agregar variables globales a todos los templates
"""

def notificaciones_no_leidas(request):
    """
    Agrega el contador de notificaciones no leídas a todos los templates
    """
    # Solo calcular si el usuario es admin (rol = 1)
    if request.session.get('usuario_rol') == 1:
        from core.models import NotificacionProblema
        total_notificaciones = NotificacionProblema.objects.filter(leida=False).count()
        return {
            'total_notificaciones_no_leidas': total_notificaciones
        }
    return {
        'total_notificaciones_no_leidas': 0
    }
