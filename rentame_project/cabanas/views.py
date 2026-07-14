from django.shortcuts import render, get_object_or_404
from .models import Cabana, Promocion, MensajeContacto


def inicio(request):
    promociones = Promocion.objects.filter(activa=True).select_related("cabana")[:6]
    cabanas = Cabana.objects.filter(disponible=True).prefetch_related("servicios")
    return render(request, "cabanas/inicio.html", {
        "promociones": promociones,
        "cabanas": cabanas,
    })


def catalogo(request):
    # RF-01: catálogo público completo
    cabanas = Cabana.objects.all().prefetch_related("servicios")
    return render(request, "cabanas/catalogo.html", {"cabanas": cabanas})


def detalle_cabana(request, clave):
    # RF-02: detalle técnico de una cabaña
    cabana = get_object_or_404(Cabana, clave=clave)
    return render(request, "cabanas/detalle.html", {"cabana": cabana})


def nosotros(request):
    # RF-04: sección informativa estática
    return render(request, "cabanas/nosotros.html")


def contacto(request):
    # RF-05: formulario de dudas
    cabanas = Cabana.objects.all()
    enviado = False
    if request.method == "POST":
        MensajeContacto.objects.create(
            nombre=request.POST.get("nombre", ""),
            correo=request.POST.get("correo", ""),
            telefono=request.POST.get("telefono", ""),
            cabana_id=request.POST.get("cabana") or None,
            mensaje=request.POST.get("mensaje", ""),
        )
        enviado = True
    return render(request, "cabanas/contacto.html", {
        "cabanas": cabanas,
        "enviado": enviado,
    })


def blog(request):
    # RF-06: visualización pública de dudas ya atendidas y aprobadas
    entradas = MensajeContacto.objects.filter(
        publicado_en_blog=True, atendido=True
    ).select_related("cabana")
    return render(request, "cabanas/blog.html", {"entradas": entradas})
