"""Script de carga de datos de ejemplo para tomar capturas de pantalla.
Ejecutar con: python manage.py shell < seed_datos.py
"""
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rentame_project.settings")
django.setup()

from datetime import date, timedelta
from cabanas.models import Servicio, Cabana, Promocion, MensajeContacto

servicios_nombres = ["Wi-Fi", "Jacuzzi", "Chimenea", "Microondas", "Estacionamiento", "Asador"]
servicios = [Servicio.objects.get_or_create(nombre=n)[0] for n in servicios_nombres]

datos_cabanas = [
    ("CAB-001", "Cabaña Bosque Alto", "Mazamitla", 2400, 4, 2),
    ("CAB-002", "Cabaña Pino Real", "Mazamitla", 2800, 6, 3),
    ("CAB-003", "Cabaña Río Claro", "Angangueo", 1900, 3, 2),
    ("CAB-004", "Cabaña Monarca", "Angangueo", 3200, 8, 4),
]

cabanas = []
for clave, nombre, ubicacion, costo, cap, camas in datos_cabanas:
    c, creada = Cabana.objects.get_or_create(
        clave=clave,
        defaults=dict(
            nombre=nombre, ubicacion=ubicacion, costo_por_dia=costo,
            capacidad_maxima=cap, numero_camas=camas,
            descripcion=f"{nombre} es una cabaña rodeada de bosque, ideal para {cap} personas.",
            promedio_calificacion=4.9, numero_resenas=12,
        )
    )
    c.servicios.set(servicios[:4])
    cabanas.append(c)

Promocion.objects.get_or_create(
    cabana=cabanas[0], titulo="Fin de semana en el bosque",
    defaults=dict(
        descripcion="20% de descuento en tu segunda noche",
        porcentaje_descuento=20,
        fecha_inicio=date.today() - timedelta(days=2),
        fecha_fin=date.today() + timedelta(days=20),
        activa=True,
    )
)

MensajeContacto.objects.get_or_create(
    nombre="Ana Torres", correo="ana@example.com",
    cabana=cabanas[0],
    mensaje="¿La cabaña acepta mascotas?",
    defaults=dict(
        respuesta="¡Sí! Aceptamos mascotas pequeñas sin costo adicional.",
        atendido=True, publicado_en_blog=True,
    )
)

print("Datos de ejemplo cargados correctamente.")
