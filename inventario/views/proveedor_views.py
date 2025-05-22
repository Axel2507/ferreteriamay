from django.shortcuts import render, redirect, get_object_or_404
from inventario.models.proveedor import Proveedor
from inventario.analizador.procesador import CommandProcessor
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q 

def listar_proveedores(request):
    query = request.GET.get('q', '')  # Obtener valor de búsqueda, por defecto vacío
    if query:
        proveedores = Proveedor.objects.filter(
            Q(activo=True) & (
                Q(nombre_empresa__icontains=query) |
                Q(nombre_contacto__icontains=query) |
                Q(correo__icontains=query)
            )
        ).order_by('nombre_empresa')
    else:
        proveedores = Proveedor.objects.filter(activo=True).order_by('nombre_empresa')

    return render(request, 'inventario/proveedor/listar_proveedores.html', {
        'proveedores': proveedores,
        'query': query  # Pasamos el valor para mostrarlo en el input de búsqueda
    })

def eliminar_proveedor(request, id_proveedor):
    """Vista para desactivar proveedor pasando por el procesador"""
    # 1. Construir el comando
    comando = f"REM PROV {id_proveedor}"

    print(f"Comando enviado al procesador: {comando}")

    # 2. Procesar el comando
    procesador = CommandProcessor()
    resultado = procesador.process(comando)

    # 3. Revisar resultado
    if resultado["success"]:
        return redirect('listar_proveedores')
    else:
        # Si hubo error, puedes mostrar un error amigable
        return render(request, 'inventario/proveedor/listar_proveedores.html', {
            'error': resultado.get("error", "Error inesperado al eliminar proveedor."),
            'proveedores': Proveedor.objects.filter(activo=True).order_by('nombre_empresa')
        })


def agregar_proveedor(request):
    if request.method == "POST":
        nombre_empresa = request.POST.get('nombre_empresa')
        nombre_contacto = request.POST.get('nombre_contacto')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')

        comando = f'ADD PROV "{nombre_empresa}" "{nombre_contacto}" {telefono} {correo} "{direccion}"'

        print("Comando enviado:", comando)

        procesador = CommandProcessor()
        resultado = procesador.process(comando)
        url = reverse('listar_proveedores')  # este sí es el nombre de la vista
        if resultado["success"]:
            return HttpResponseRedirect(f'{url}?success=1')
        else:
            return render(request, 'inventario/proveedor/agregar_proveedor.html', {
                'error': resultado["error"]
            })

    return render(request, 'inventario/proveedor/agregar_proveedor.html')   

def formatear_telefono(numero):
    """Formatea un número de 10 dígitos como (###)###-####"""
    numero = numero.strip()
    if len(numero) == 10 and numero.isdigit():
        return f"({numero[:3]}){numero[3:6]}-{numero[6:]}"
    return numero  # Devuelve tal cual si ya está formateado o no tiene 10 dígitos

def actualizar_proveedor(request, id):
    """Vista para actualizar un proveedor existente pasando por el procesador"""
    # Obtener el proveedor existente
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)

    if request.method == "POST":
        # Obtener datos del formulario
        nombre_empresa = request.POST.get('nombre_empresa')
        nombre_contacto = request.POST.get('nombre_contacto')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')

        print("POST recibido:", request.POST)

        # Formatear el teléfono
        telefono = formatear_telefono(telefono)

        # Verificar que todos los campos requeridos están presentes
        campos_requeridos = [nombre_empresa, nombre_contacto, telefono, correo, direccion]
        if any(campo is None or campo == "" for campo in campos_requeridos):
            return render(request, 'inventario/proveedor/actualizar_proveedor.html', {
                'proveedor': proveedor,
                'error': 'Todos los campos son obligatorios.'
            })

        # Crear el comando en el formato correcto
        comando = f'ACT PROV I{id} "{nombre_empresa}" "{nombre_contacto}" {telefono} {correo} "{direccion}"'
        procesador = CommandProcessor()
        resultado = procesador.process(comando)

        if resultado["success"]:
            return redirect('listar_proveedores')
        else:
            return render(request, 'inventario/proveedor/actualizar_proveedor.html', {
                'proveedor': proveedor,
                'error': resultado.get("error", "Error inesperado al actualizar proveedor.")
            })

    return render(request, 'inventario/proveedor/actualizar_proveedor.html', {
        'proveedor': proveedor
    })

def eliminar_proveedor(request, id):
    if request.method == "POST":
        proveedor = get_object_or_404(Proveedor, id=id)
        proveedor.delete()
        return redirect('listar_proveedores')