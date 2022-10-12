from django.db import models

class Empresa(models.model):
    nombre_empresa = models.CharField(max_length = 100)
    sector_empresa = models.CharField(max_length = 100)
    fecha_creacion = models.DateTimeField(auto_now_add =True)
    def __str__(self) -> str:
        return self.nombre_empresa
    