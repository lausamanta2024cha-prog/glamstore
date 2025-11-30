from django.db import models


class NotificacionProblema(models.Model):
    idNotificacion = models.AutoField(primary_key=True)
    idPedido = models.ForeignKey(
        'core.Pedido',
        on_delete=models.CASCADE,
        db_column='idPedido'
    )
    motivo = models.TextField()
    foto = models.ImageField(upload_to='problemas_entrega/', null=True, blank=True)
    fechaReporte = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    respuesta_admin = models.TextField(null=True, blank=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notificaciones_problema'
        managed = True  # Django puede crear esta tabla
        app_label = 'core'
        ordering = ['-fechaReporte']
    
    def __str__(self):
        return f"Problema Pedido #{self.idPedido_id} - {self.fechaReporte}"


class NotificacionReporte(models.Model):
    idNotificacion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    contenido_html = models.TextField()
    tipo = models.CharField(max_length=50, default='DASHBOARD')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notificaciones_reporte'
        managed = True
        app_label = 'core'
        ordering = ['-fechaCreacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.fechaCreacion}"
