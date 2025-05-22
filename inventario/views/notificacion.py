from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from inventario.models.notificacion import Notificacion
from django.db import connection
from io import BytesIO
import datetime
import pandas as pd



def obtener_notificaciones(request):
    notificaciones = Notificacion.objects.all()[:5]
    data = [
        {"id": n.id, "mensaje": n.mensaje, "fecha": n.fecha.strftime('%Y-%m-%d %H:%M')}
        for n in notificaciones
    ]
    return JsonResponse({"notificaciones": data})

def verificar_caducidad(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("CALL VerificarCaducidadProductos()");
        return redirect('verificar_caducidad')

    notificaciones = Notificacion.objects.filter(mensaje__icontains='caduca').order_by('-fecha')[:10]
    return render(request, 'verificar_caducidad.html', {"notificaciones": notificaciones})

def generar_reporte(request):
    resultados = []
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']

        with connection.cursor() as cursor:
            cursor.execute("CALL GenerarReporteVentas(%s, %s)", [fecha_inicio, fecha_fin])
            cursor.execute("SELECT id_venta, nombre_material, cantidad, fecha_venta FROM inventario_reporteventassemanal WHERE fecha_venta BETWEEN %s AND %s", [fecha_inicio, fecha_fin])
            resultados = cursor.fetchall()

    return render(request, 'reporte_ventas.html', {"resultados": resultados})

def exportar_excel(request):
    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_venta, nombre_material, cantidad, fecha_venta FROM inventario_reporteventassemanal WHERE fecha_venta BETWEEN %s AND %s", [fecha_inicio, fecha_fin])
        rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=['ID Venta', 'Material', 'Cantidad', 'Fecha'])
    buffer = BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Reporte')
    writer.close()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ReporteVentas.xlsx'
    return response
