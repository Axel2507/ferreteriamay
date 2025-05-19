from django.shortcuts import render, redirect
from inventario.models.categoria import Categoria
from inventario.analizador.procesador import CommandProcessor
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect


def agregar_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        abreviacion = request.POST.get('abreviacion')

        # Construir comando para el Lexer
        comando = f'ADD CAT "{nombre}" {abreviacion.upper()}'
        
        print("Comando enviado al procesador:", comando)

        procesador = CommandProcessor()
        resultado = procesador.process(comando)
        print("Resultado del procesador:", resultado)

        url = reverse('listar_categorias')  # este sí es el nombre de la vista
        if resultado["success"]:
            return HttpResponseRedirect(f'{url}?success=1') # Redirige al listado de categorías
        else:
            categorias = Categoria.objects.all().order_by('nombre')
            return render(request, 'inventario/categoria/agregar_categoria.html', {
                'error': resultado["error"],
                'categorias': categorias
            })

    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'inventario/categoria/agregar_categoria.html', {
        'categorias': categorias
    })

def listar_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')  # Ordenadas por nombre

    context = {
        'categorias': categorias
    }

    return render(request, 'inventario/categoria/listar_categorias.html', context)

def actualizar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == "POST":
        nombre = request.POST.get('nombre')
        abreviacion = request.POST.get('abreviacion')

        campos_requeridos = [nombre, abreviacion]
        if any(campo is None or campo.strip() == "" for campo in campos_requeridos):
            return render(request, 'inventario/categoria/actualizar_categoria.html', {
                'categoria': categoria,
                'error': 'Todos los campos son obligatorios.'
            })

        comando = f'ACT CAT I{categoria.id} "{nombre}" {abreviacion.upper()}'
        print("Comando enviado al procesador:", comando)

        procesador = CommandProcessor()
        resultado = procesador.process(comando)
        print("Resultado del procesador:", resultado)

        if resultado["success"]:
            return redirect('listar_categorias')
        else:
            return render(request, 'inventario/categoria/actualizar_categoria.html', {
                'categoria': categoria,
                'error': resultado["error"]
            })

    return render(request, 'inventario/categoria/actualizar_categoria.html', {
        'categoria': categoria
    })