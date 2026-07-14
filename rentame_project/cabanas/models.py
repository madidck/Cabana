from django.db import models
from django.utils import timezone


class Servicio(models.Model):
    """Catálogo de servicios que puede incluir una cabaña (Wi-Fi, jacuzzi, etc.)"""
    nombre = models.CharField(max_length=50, unique=True)
    icono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Nombre de ícono (ej. bi-wifi de Bootstrap Icons)"
    )
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Cabana(models.Model):
    """Catálogo y CRUD de cabañas."""
    clave = models.CharField(max_length=10, unique=True, help_text="Clave interna, ej. CAB-001")
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, default="Mazamitla")
    descripcion = models.TextField(blank=True)
    costo_por_dia = models.DecimalField(max_digits=8, decimal_places=2)
    capacidad_maxima = models.PositiveSmallIntegerField()
    numero_camas = models.PositiveSmallIntegerField()
    imagen = models.ImageField(upload_to="cabanas/", blank=True, null=True)
    servicios = models.ManyToManyField(Servicio, blank=True, related_name="cabanas")
    disponible = models.BooleanField(default=True)
    promedio_calificacion = models.DecimalField(
        max_digits=3, decimal_places=2, default=0,
        help_text="Se recalcula automáticamente con las reseñas (RF-12)"
    )
    numero_resenas = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Cabaña"
        verbose_name_plural = "Cabañas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.clave} - {self.nombre}"


class Promocion(models.Model):
    """Promociones vigentes del mes."""
    cabana = models.ForeignKey(Cabana, on_delete=models.CASCADE, related_name="promociones")
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    porcentaje_descuento = models.PositiveSmallIntegerField(default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.titulo} ({self.cabana.nombre})"

    def vigente(self):
        hoy = timezone.now().date()
        return self.activa and self.fecha_inicio <= hoy <= self.fecha_fin
    vigente.boolean = True


class MensajeContacto(models.Model):
    """Formulario de dudas y moderación de mensajes."""
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    cabana = models.ForeignKey(
        Cabana, on_delete=models.SET_NULL, null=True, blank=True, related_name="mensajes"
    )
    mensaje = models.TextField()
    respuesta = models.TextField(blank=True)
    publicado_en_blog = models.BooleanField(default=False)
    atendido = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ["-fecha_envio"]

    def __str__(self):
        return f"{self.nombre} - {self.cabana}"
