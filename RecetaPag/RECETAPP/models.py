from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Receta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    ingredientes = models.TextField()
    pasos = models.TextField()
    video = models.FileField(upload_to='videos_recetas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class comentario(models.Model):
    receta = models.ForeignKey(Receta, related_name='comentarios', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    calificacion = models.IntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)
    
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    receta = models.ForeignKey('Receta', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'receta')  # Evita duplicados

    def __str__(self):
        return f"{self.usuario.username} - {self.receta.titulo}"