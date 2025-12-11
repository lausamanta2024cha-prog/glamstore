

def notificaciones_no_leidas(request):
    try:
        # Solo calcular si el usuario es admin (rol = 1)
        if request.session.get('usuario_rol') == 1:
            from core.models import NotificacionProblema
            total_notificaciones = NotificacionProblema.objects.filter(leida=False).count()
            return {
                'total_notificaciones_no_leidas': total_notificaciones
            }
    except Exception:
        pass
    
    return {
        'total_notificaciones_no_leidas': 0
    }
