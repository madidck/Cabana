from django.contrib import admin
from .models import Servicio, Cabana, Promocion, MensajeContacto

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "icono")
    search_fields = ("nombre",)

class PromocionInline(admin.TabularInline):
    """Permite crear/editar promociones directamente desde la cabaña (RF-09)."""
    model = Promocion
    extra = 0
    fields = ("titulo", "porcentaje_descuento", "fecha_inicio", "fecha_fin", "activa")

@admin.register(Cabana)
class CabanaAdmin(admin.ModelAdmin):
    
    list_display = (
        "clave", "nombre", "ubicacion", "costo_por_dia",
        "capacidad_maxima", "disponible", "promedio_calificacion",
    )
    list_filter = ("disponible", "ubicacion", "servicios")
    search_fields = ("clave", "nombre", "ubicacion")
    autocomplete_fields = ("servicios",)
    readonly_fields = (
        "fecha_registro", "fecha_actualizacion",
        "promedio_calificacion", "numero_resenas",
    )
    inlines = [PromocionInline]
    fieldsets = (
        ("Identificación", {
            "fields": ("clave", "nombre", "ubicacion", "disponible")
        }),
        ("Detalle técnico", {
            "fields": ("descripcion", "costo_por_dia", "capacidad_maxima",
                       "numero_camas", "servicios", "imagen")
        }),
        ("Calificaciones (solo lectura)", {
            "fields": ("promedio_calificacion", "numero_resenas"),
            "classes": ("collapse",),
        }),
        ("Auditoría", {
            "fields": ("fecha_registro", "fecha_actualizacion"),
            "classes": ("collapse",),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("clave",)
        return self.readonly_fields

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "cabana", "porcentaje_descuento",
                    "fecha_inicio", "fecha_fin", "activa", "vigente")
    list_filter = ("activa", "cabana")
    search_fields = ("titulo", "cabana__nombre")
    autocomplete_fields = ("cabana",)

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    
    list_display = ("nombre", "correo", "cabana", "atendido",
                    "publicado_en_blog", "fecha_envio")
    list_filter = ("atendido", "publicado_en_blog", "fecha_envio")
    search_fields = ("nombre", "correo", "mensaje")
    autocomplete_fields = ("cabana",)
    readonly_fields = ("nombre", "correo", "telefono", "cabana", "mensaje", "fecha_envio")
    fieldsets = (
        ("Datos del solicitante", {
            "fields": ("nombre", "correo", "telefono", "cabana", "mensaje", "fecha_envio")
        }),
        ("Gestión administrativa", {
            "fields": ("respuesta", "atendido", "publicado_en_blog", "fecha_respuesta")
        }),
    )
