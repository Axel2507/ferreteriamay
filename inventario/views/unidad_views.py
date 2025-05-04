from django.shortcuts import render, redirect
from inventario.models.unidad import Unidad
from inventario.analizador.procesador import CommandProcessor

def listar_unidades(request):
    """Vista para listar todas las unidades activas"""
    unidades = Unidad.objects.filter(activo=True).order_by('nombre')
    return render(request, 'inventario/unidad/listar_unidades.html', {'unidades': unidades})

def eliminar_unidad(request, unidad_id):
    """Vista para desactivar una unidad"""
    unidad = Unidad.objects.get(id=unidad_id)
    unidad.activo = False
    unidad.save()
    return redirect('listar_unidades')

def agregar_unidad(request):
    """Vista para agregar una nueva unidad pasando por los analizadores"""
    
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        abreviacion = request.POST.get('abreviacion')

        if nombre and abreviacion:
            comando = f'ADD UNI "{nombre}" {abreviacion}'
            print("Comando enviado:", comando)

            procesador = CommandProcessor()
            resultado = procesador.process(comando)

            if resultado["success"]:
                return redirect('listar_unidades')
            else:
                unidades = Unidad.objects.filter(activo=True).order_by('nombre')
                return render(request, 'inventario/unidad/agregar_unidad.html', {
                    'error': resultado["error"],
                    'unidades': unidades
                })
        else:
            unidades = Unidad.objects.filter(activo=True).order_by('nombre')
            return render(request, 'inventario/unidad/agregar_unidad.html', {
                'error': 'Todos los campos son obligatorios.',
                'unidades': unidades
            })

    unidades = Unidad.objects.filter(activo=True).order_by('nombre')
    return render(request, 'inventario/unidad/agregar_unidad.html', {
        'unidades': unidades
    })