from django.db import models

# Create your models here.
class Url(models.Model):
    nombre = models.CharField(max_length=64)
    def __str__(self):
        return self.nombre
