from django.shortcuts import render, redirect
from inventario.models.categoria import Categoria
from inventario.analizador.procesador import CommandProcessor
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages


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
    query = request.GET.get('q')  # Tomamos el parámetro de búsqueda

    if query:
        categorias = Categoria.objects.filter(
            Q(nombre__icontains=query) | Q(abreviacion__icontains=query)
        ).order_by('nombre')
    else:
        categorias = Categoria.objects.all().order_by('nombre')

    context = {
        'categorias': categorias,
        'query': query,  # Pasamos query para mostrar en la caja de búsqueda
    }

    return render(request, 'inventario/categoria/listar_categorias.html', context)

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


def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    messages.success(request, "Categoría eliminada correctamente.")
    return redirect('listar_categorias')