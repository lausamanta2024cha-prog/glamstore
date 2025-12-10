from django.db import models

class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=255, null=True)
    id_rol = models.IntegerField()
    idCliente = models.IntegerField(null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=False)
    nombre = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=20, null=True)
    direccion = models.CharField(max_length=50, null=True)
    reset_token = models.CharField(max_length=255, null=True)
    reset_token_expires = models.DateTimeField(null=True)
    ultimoAcceso = models.DateTimeField(null=True, blank=True, db_column='ultimoAcceso')

    class Meta:
        db_table = 'usuarios'
        managed = False
        app_label = 'core'
