from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import datetime
from inventario.models.venta import Venta, DetalleVenta
from inventario.models.devolucion import Devolucion
from inventario.models.devolucion import DetalleDevolucion
from inventario.models.material import Material

def agregar_devolucion(request):
    """Vista principal para registrar una devolución"""
    return render(request, 'inventario/devolucion/agregar_devolucion.html')

def buscar_venta(request):
    """Busca ventas por ID o fecha"""
    venta_id = request.GET.get('venta_id')
    fecha_venta = request.GET.get('fecha_venta')
    
    if venta_id:
        try:
            venta = Venta.objects.get(id=venta_id)
            return redirect('seleccionar_venta', venta_id=venta.id)
        except Venta.DoesNotExist:
            return render(request, 'inventario/devolucion/agregar_devolucion.html', {
                'venta_id': venta_id
            })
    elif fecha_venta:
        try:
            fecha = datetime.datetime.strptime(fecha_venta, '%Y-%m-%d').date()
            ventas = Venta.objects.filter(fecha__date=fecha)
            if ventas.exists():
                return render(request, 'inventario/devolucion/agregar_devolucion.html', {
                    'ventas': ventas,
                    'fecha_venta': fecha_venta
                })
            else:
                return render(request, 'inventario/devolucion/agregar_devolucion.html', {
                    'fecha_venta': fecha_venta
                })
        except ValueError:
            messages.error(request, 'Formato de fecha inválido')
            return redirect('agregar_devolucion')
    
    return redirect('agregar_devolucion')

def seleccionar_venta(request, venta_id):
    # Obtener la venta y sus detalles
    venta = Venta.objects.get(id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta).select_related('material')
    
    # Calcular precio unitario para cada detalle
    for detalle in detalles:
        try:
            # Calcular precio unitario = subtotal / cantidad
            detalle.precio_unitario = round(detalle.subtotal / detalle.cantidad, 2)
        except (AttributeError, ZeroDivisionError):
            detalle.precio_unitario = 0
    
    context = {
        'venta': venta,
        'detalles': detalles,
        'venta_id': venta_id,  # Asegúrate de pasar esto al contexto
    }
    
    return render(request, 'inventario/devolucion/agregar_devolucion.html', context)


@transaction.atomic
def procesar_devolucion(request):
    if request.method == 'POST':
        venta_id = request.POST.get('venta_id')
        motivo = request.POST.get('motivo')
        
        venta = get_object_or_404(Venta, id=venta_id)
        detalles = DetalleVenta.objects.filter(venta=venta)
        
        devolucion = Devolucion.objects.create(
            venta=venta,
            fecha=timezone.now(),
            motivo=motivo
        )
        
        total_devolucion = Decimal('0.00')
        items_devueltos = False
        
        for detalle in detalles:
            cantidad_name = f'cantidad_{detalle.id}'
            try:
                cantidad_devuelta = int(request.POST.get(cantidad_name, 0))
            except (TypeError, ValueError):
                cantidad_devuelta = 0

            if 0 < cantidad_devuelta <= detalle.cantidad:
                subtotal = detalle.material.precio_venta * Decimal(cantidad_devuelta)

                DetalleDevolucion.objects.create(
                    devolucion=devolucion,
                    detalle_venta=detalle,
                    cantidad_devuelta=cantidad_devuelta
                )

                material = detalle.material
                material.stock += cantidad_devuelta
                material.save()

                total_devolucion += subtotal
                items_devueltos = True

        if not items_devueltos:
            devolucion.delete()
            messages.error(request, 'Debe devolver al menos un producto con cantidad mayor a 0.')
            return redirect('seleccionar_venta', venta_id=venta_id)

        messages.success(request, f'Devolución registrada con un total de ${total_devolucion:.2f}.')
        return redirect('listar_devoluciones')

    return redirect('agregar_devolucion')

def listar_devoluciones(request):
    devoluciones = Devolucion.objects.all().order_by('-fecha')  # Ordena por fecha descendente
    context = {'devoluciones': devoluciones}
    return render(request, 'inventario/devolucion/listar_devolucion.html', context)


def ver_devolucion(request, devolucion_id):
    """Muestra los detalles de una devolución específica"""
    devolucion = get_object_or_404(Devolucion, id=devolucion_id)
    detalles_devolucion = DetalleDevolucion.objects.filter(devolucion=devolucion)
    
    return render(request, 'inventario/devolucion/confirmacion_devolucion.html', {
        'devolucion': devolucion,
        'detalles_devolucion': detalles_devolucion
    })