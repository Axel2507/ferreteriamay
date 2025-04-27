from django.shortcuts import render, redirect
from inventario.models.material import Material
from inventario.models.categoria import Categoria
from inventario.models.proveedor import Proveedor
from inventario.models.unidad import Unidad

def agregar_material(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        stock_minimo = request.POST.get('stock_minimo')
        categoria_id = request.POST.get('categoria')
        proveedor_id = request.POST.get('proveedor')
        unidad_id = request.POST.get('unidad')
        fecha_caducidad = request.POST.get('fecha_caducidad') or None

        Material.objects.create(
            codigo=codigo,
            nombre=nombre,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            stock_minimo=stock_minimo,
            categoria_id=categoria_id,
            proveedor_id=proveedor_id,
            unidad_id=unidad_id,
            fecha_caducidad=fecha_caducidad
        )

        return redirect('listar_materiales')  # Después configuramos esta vista

    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    unidades = Unidad.objects.all()

    context = {
        'categorias': categorias,
        'proveedores': proveedores,
        'unidades': unidades
    }
    return render(request, 'inventario/material/agregar_material.html', context)
