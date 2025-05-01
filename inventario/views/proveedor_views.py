from django.shortcuts import render, redirect, get_object_or_404
from inventario.models.proveedor import Proveedor
from inventario.analizador.procesador import CommandProcessor
from django.urls import reverse
from django.http import HttpResponseRedirect

def listar_proveedores(request):
    """Vista para listar todos los proveedores activos"""
    proveedores = Proveedor.objects.filter(activo=True).order_by('nombre_empresa')
    return render(request, 'inventario/proveedor/listar_proveedores.html', {'proveedores': proveedores})

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
