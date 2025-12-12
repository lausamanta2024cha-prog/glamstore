from django.db import models

class MensajeContacto(models.Model):
    idMensaje = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensajes_contacto'
        managed = False
        app_label = 'core'