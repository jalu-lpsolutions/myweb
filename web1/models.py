from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    padre = models.ForeignKey(User, null=True, blank=True, related_name='hijos', on_delete=models.SET_NULL)

    def __str__(self):
        return self.usuario.username

class Customer(models.Model):

    CUSTOMER_TYPE = {
    "D": "DOMESTICO",
    "P": "PYME",
    "A": "AUTONOMO",
    "I": "INDUSTRIAL",
}

    creation_time = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=10,null=True)
    cif = models.CharField(max_length=9)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20)
    nombre_completo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=12)
    movil = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    customer_type = models.CharField(max_length=50,choices=CUSTOMER_TYPE)
    direccion = models.CharField(max_length=50,null=True)
    codigo_postal = models.CharField(max_length=5,null=True)
    poblacion = models.CharField(max_length=50,null=True)
    municipio = models.CharField(max_length=50,null=True)
    provincia = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.cif

class Serial_number(models.Model):
    type_code = models.CharField(max_length=4)
    year = models.IntegerField()
    count = models.IntegerField()
    code = models.CharField(max_length=10)
    def __str__(self):
        return self.code