from django.db import models

class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True, db_column='idusuario')
    email = models.CharField(max_length=30, unique=True, db_column='email')
    password = models.CharField(max_length=255, null=True, db_column='password')
    id_rol = models.IntegerField(db_column='id_rol')
    idCliente = models.IntegerField(null=True, db_column='idcliente')
    fechaCreacion = models.DateTimeField(auto_now_add=False, db_column='fechacreacion')
    nombre = models.CharField(max_length=50, null=True, db_column='nombre')
    telefono = models.CharField(max_length=20, null=True, db_column='telefono')
    direccion = models.CharField(max_length=50, null=True, db_column='direccion')
    reset_token = models.CharField(max_length=255, null=True, db_column='reset_token')
    reset_token_expires = models.DateTimeField(null=True, db_column='reset_token_expires')
    ultimoAcceso = models.DateTimeField(null=True, blank=True, db_column='ultimoacceso')

    class Meta:
        db_table = 'usuarios'
        managed = False
        app_label = 'core'
