from django.db import models


class NotificacionProblema(models.Model):
    idNotificacion = models.AutoField(primary_key=True, db_column='idnotificacion')
    idPedido = models.ForeignKey(
        'core.Pedido',
        on_delete=models.CASCADE,
        db_column='idpedido'
    )
    motivo = models.TextField(db_column='motivo')
    foto = models.ImageField(upload_to='problemas_entrega/', null=True, blank=True, db_column='foto')
    fechaReporte = models.DateTimeField(auto_now_add=True, db_column='fechareporte')
    leida = models.BooleanField(default=False, db_column='leida')
    respuesta_admin = models.TextField(null=True, blank=True, db_column='respuesta_admin')
    fecha_respuesta = models.DateTimeField(null=True, blank=True, db_column='fecha_respuesta')
    
    class Meta:
        db_table = 'notificaciones_problema'
        managed = True  # Django puede crear esta tabla
        app_label = 'core'
        ordering = ['-fechaReporte']
    
    def __str__(self):
        return f"Problema Pedido #{self.idPedido_id} - {self.fechaReporte}"


class NotificacionReporte(models.Model):
    idNotificacion = models.AutoField(primary_key=True, db_column='idnotificacion')
    titulo = models.CharField(max_length=255, db_column='titulo')
    contenido_html = models.TextField(db_column='contenido_html')
    tipo = models.CharField(max_length=50, default='DASHBOARD', db_column='tipo')
    fechaCreacion = models.DateTimeField(auto_now_add=True, db_column='fechacreacion')
    leida = models.BooleanField(default=False, db_column='leida')
    
    class Meta:
        db_table = 'notificaciones_reporte'
        managed = True
        app_label = 'core'
        ordering = ['-fechaCreacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.fechaCreacion}"
