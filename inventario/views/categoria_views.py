from django.shortcuts import render, redirect
from inventario.models.categoria import Categoria
from inventario.analizador.procesador import CommandProcessor

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

        if resultado["success"]:
            return redirect('registrar_categoria?success=1')  # Redirige al listado de categorías
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