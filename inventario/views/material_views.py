from django.shortcuts import render, redirect
from inventario.models.material import Material
from inventario.models.categoria import Categoria
from inventario.models.proveedor import Proveedor
from inventario.models.unidad import Unidad
from inventario.analizador.procesador import CommandProcessor

def agregar_material(request):
    """Vista para agregar un material pasando por analizadores"""
    categorias = Categoria.objects.filter(activa=True)
    proveedores = Proveedor.objects.filter(activo=True)
    unidades = Unidad.objects.filter(activo=True)

    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        stock_minimo = request.POST.get('stock_minimo')
        categoria_id = request.POST.get('categoria')
        proveedor_id = request.POST.get('proveedor')
        unidad_compra_id = request.POST.get('unidad_compra')
        unidad_venta_id = request.POST.get('unidad_venta')
        factor_conversion = request.POST.get('factor_conversion')
        fecha_caducidad = request.POST.get('fecha_caducidad') 

        print("POST recibido:", request.POST)

        campos_requeridos = [codigo, nombre, precio_compra, precio_venta, stock, stock_minimo, categoria_id, proveedor_id, unidad_compra_id, unidad_venta_id, factor_conversion]
        if any(campo is None or campo == "" for campo in campos_requeridos):

            return render(request, 'inventario/material/agregar_material.html', {
                'categorias': categorias,
                'proveedores': proveedores,
                'unidades': unidades,
                'error': 'Todos los campos son obligatorios, excepto fecha de caducidad.'
            })
        
        fecha_caducidad_token = fecha_caducidad if fecha_caducidad else 'NULL'

        comando = f'ADD MAT C{codigo} "{nombre}" ${precio_compra} ${precio_venta} {stock} {stock_minimo} I{categoria_id} I{proveedor_id} I{unidad_compra_id} I{unidad_venta_id} {factor_conversion} {fecha_caducidad_token}'
        print("Comando enviado:", comando)

        procesador = CommandProcessor()
        resultado = procesador.process(comando)

        if resultado["success"]:
            return redirect('listar_materiales')
        else:
            return render(request, 'inventario/material/agregar_material.html', {
                'categorias': categorias,
                'proveedores': proveedores,
                'unidades': unidades,
                'error': resultado["error"]
            })

    return render(request, 'inventario/material/agregar_material.html', {
        'categorias': categorias,
        'proveedores': proveedores,
        'unidades': unidades
    })

def listar_materiales(request):
    """Vista para listar todos los materiales disponibles"""
    materiales = Material.objects.select_related("categoria", "proveedor","unidad_compra", "unidad_venta").order_by("nombre")
    return render(request, 'inventario/material/listar_materiales.html', {"materiales": materiales})