# views/material_views.py o views/venta_views.py
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from inventario.analizador.procesador import CommandProcessor
from django.http import JsonResponse
from inventario.models.material import Material
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from inventario.models import Venta
from inventario.models.venta import DetalleVenta

def agregar_venta(request):
    """Vista para registrar una venta usando el analizador y carrito"""
    if request.method == "POST":
        detalle_json = request.POST.get("detalle_venta")

        if not detalle_json:
            return render(request, 'inventario/venta/agregar_venta.html', {
                "error": "No se recibieron datos de la venta."
            })

        try:
            detalle = json.loads(detalle_json)
            total = detalle.get("total")
            items = detalle.get("items")

            if not items or float(total) <= 0:
                return render(request, 'inventario/venta/agregar_venta.html', {
                    "error": "Carrito vacío o total inválido."
                })
            
            total_formateado = f"{total:.2f}"

            procesador = CommandProcessor()
            print("Detalle recibido:", detalle_json)
            # Crear venta
            comando_venta = f"ADD VEN ${total_formateado}"
            resultado_venta = procesador.process(comando_venta)

            if not resultado_venta.get("success"):
                return render(request, 'inventario/venta/agregar_venta.html', {
                    "error": resultado_venta.get("error")
                })

            venta_id = resultado_venta.get("object").get("id")

            # Agregar detalle de venta
            for item in items:
                subtotal = float(item['subtotal'])
                subtotal_formateado = f"{subtotal:.2f}"
                comando_detalle = f"ADD DVEN I{venta_id} C{item['codigo']} {item['cantidad']} ${subtotal_formateado}"
                resultado_item = procesador.process(comando_detalle)

                if not resultado_item.get("success"):
                    raise Exception(f"Error al agregar detalle: {resultado_item.get('error')}")

            return redirect('ticket_venta', venta_id=venta_id)

        except Exception as e:
            return render(request, 'inventario/venta/agregar_venta.html', {
                "error": f"Error inesperado: {str(e)}"
            })

    return render(request, 'inventario/venta/agregar_venta.html')


def buscar_materiales(request):
    consulta = request.GET.get('q', '')
    resultados = []

    if consulta:
        materiales = Material.objects.filter(
            activo=True
        ).filter(
             Q(nombre__icontains=consulta) | Q(codigo__icontains=consulta)
        )[:10]

        for m in materiales:
            resultados.append({
                "id": m.codigo,
                "nombre": m.nombre,
                "precio": float(m.precio_venta),
                "unidad": m.unidad_venta.abreviacion if m.unidad_venta else "",
                "stock": m.stock
            })

    return JsonResponse(resultados, safe=False)

def ticket_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta).select_related('material')

    return render(request, 'inventario/venta/ticket_venta.html', {
        'venta': venta,
        'detalles': detalles,
        })