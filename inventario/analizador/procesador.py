from .lexer import Lexer, LexerError
from .parser import Parser, SyntaxError
from .semantic import SemanticAnalyzer, SemanticError
from django.db import transaction
from inventario.models import Material, Categoria, Proveedor, Unidad, Venta, Devolucion, Descuento
from django.db.models import F

class CommandProcessor:
    def __init__(self):
        pass
    
    def process(self, command_str):
        """Procesa un comando completo pasándolo por los analizadores y ejecutando la acción"""
        try:
            # 1. Análisis léxico
            lexer = Lexer(command_str)
            tokens = lexer.analizar()
            
            # 2. Análisis sintáctico
            parser = Parser(tokens)
            parsed_data = parser.parse()
            
            # 3. Análisis semántico
            semantic = SemanticAnalyzer(parsed_data)
            semantic.analyze()
            
            # 4. Ejecución del comando
            return self.execute_command(parsed_data)
            
        except LexerError as e:
            return {"success": False, "error": f"Error léxico: {str(e)}"}
        except SyntaxError as e:
            return {"success": False, "error": f"Error sintáctico: {str(e)}"}
        except SemanticError as e:
            return {"success": False, "error": f"Error semántico: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Error inesperado: {str(e)}"}
    
    @transaction.atomic
    def execute_command(self, parsed_data):
        """Ejecuta el comando validado según su tipo y entidad"""
        command = parsed_data.get("command")
        entity = parsed_data.get("entity")
        
        method_name = f"execute_{command.lower()}_{entity.lower()}"
        if hasattr(self, method_name):
            executor_method = getattr(self, method_name)
            return executor_method(parsed_data.get("data", {}))
        else:
            return {"success": False, "error": f"No existe un ejecutor para {command} {entity}"}
    
    # Métodos de ejecución de comandos
    
    def execute_add_mat(self, data):
        """Ejecuta la adición de un material"""
        # Obtener objetos relacionados
        categoria = Categoria.objects.get(id=data.get("categoria_id"))
        proveedor = Proveedor.objects.get(id_proveedor=data.get("proveedor_id"))
        unidad = Unidad.objects.get(id=data.get("unidad_id"))
        
        # Crear nuevo material
        material = Material(
            codigo=data.get("codigo"),
            nombre=data.get("nombre"),
            descripcion=data.get("descripcion", ""),
            precio_compra=data.get("precio_compra"),
            precio_venta=data.get("precio_venta"),
            stock=data.get("stock", 0),
            stock_minimo=data.get("stock_minimo", 0),
            categoria=categoria,
            proveedor=proveedor,
            unidad=unidad
        )
        
        # Guardar y retornar éxito
        material.save()
        return {
            "success": True, 
            "message": f"Material '{data.get('nombre')}' creado correctamente con código '{data.get('codigo')}'",
            "object": {
                "codigo": material.codigo,
                "nombre": material.nombre,
                "precio_venta": float(material.precio_venta),
                "stock": material.stock
            }
        }
    
    def execute_add_cat(self, data):
        """Ejecuta la adición de una categoría"""
        print("Datos recibidos para crear categoría:", data)
        # Crear nueva categoría
        categoria = Categoria(
            nombre=data.get("nombre"),
            abreviacion=data.get("abreviacion"),
            activa=data.get("activa", True)
        )
        
        # Guardar y retornar éxito
        categoria.save()
        return {
            "success": True, 
            "message": f"Categoría '{data.get('nombre')}' creada correctamente con ID {categoria.id}",
            "object": {
                "id": categoria.id,
                "nombre": categoria.nombre,
                "abreviacion": categoria.abreviacion,
                "activa": categoria.activa
            }
        }
    
    def execute_add_ven(self, data):
        """Ejecuta la adición de una venta"""
        # Crear nueva venta
        venta = Venta(
            total=data.get("total")
        )
        
        # Guardar y retornar éxito
        venta.save()
        return {
            "success": True, 
            "message": f"Venta creada correctamente con ID {venta.id}",
            "object": {
                "id": venta.id,
                "fecha": venta.fecha.strftime('%d/%m/%Y %H:%M'),
                "total": float(venta.total)
            }
        }
    
    def execute_add_dev(self, data):
        """Ejecuta la adición de una devolución"""
        # Obtener venta relacionada
        venta = Venta.objects.get(id=data.get("venta_id"))
        
        # Crear nueva devolución
        devolucion = Devolucion(
            venta=venta,
            motivo=data.get("motivo", ""),
            fecha=data.get("fecha"),
            estado=data.get("estado", "pendiente")
        )
        
        # Guardar y retornar éxito
        devolucion.save()
        return {
            "success": True, 
            "message": f"Devolución creada correctamente con ID {devolucion.id} para la venta {venta.id}",
            "object": {
                "id": devolucion.id,
                "venta_id": venta.id,
                "fecha": devolucion.fecha.strftime('%d/%m/%Y'),
                "estado": devolucion.estado
            }
        }
    
    def execute_act_mat(self, data):
        """Ejecuta la actualización de un material"""
        # Obtener el material a actualizar
        material = Material.objects.get(codigo=data.get("codigo"))
        
        # Actualizar campos básicos
        if "nombre" in data:
            material.nombre = data.get("nombre")
        if "descripcion" in data:
            material.descripcion = data.get("descripcion")
        if "precio_compra" in data:
            material.precio_compra = data.get("precio_compra")
        if "precio_venta" in data:
            material.precio_venta = data.get("precio_venta")
        if "stock" in data:
            material.stock = data.get("stock")
        if "stock_minimo" in data:
            material.stock_minimo = data.get("stock_minimo")
        
        # Actualizar relaciones
        if "categoria_id" in data:
            material.categoria = Categoria.objects.get(id=data.get("categoria_id"))
        if "proveedor_id" in data:
            material.proveedor = Proveedor.objects.get(id_proveedor=data.get("proveedor_id"))
        if "unidad_id" in data:
            material.unidad = Unidad.objects.get(id=data.get("unidad_id"))
        
        # Guardar y retornar éxito
        material.save()
        return {
            "success": True, 
            "message": f"Material '{material.nombre}' actualizado correctamente",
            "object": {
                "codigo": material.codigo,
                "nombre": material.nombre,
                "precio_venta": float(material.precio_venta),
                "stock": material.stock
            }
        }
    
    def execute_act_cat(self, data):
        """Ejecuta la actualización de una categoría"""
        # Obtener la categoría a actualizar
        categoria = Categoria.objects.get(id=data.get("id"))
        
        # Actualizar campos
        if "nombre" in data:
            categoria.nombre = data.get("nombre")
        if "descripcion" in data:
            categoria.descripcion = data.get("descripcion")
        if "activa" in data:
            categoria.activa = data.get("activa")
        
        # Guardar y retornar éxito
        categoria.save()
        return {
            "success": True, 
            "message": f"Categoría '{categoria.nombre}' actualizada correctamente",
            "object": {
                "id": categoria.id,
                "nombre": categoria.nombre,
                "activa": categoria.activa
            }
        }
    
    def execute_rem_cat(self, data):
        """Ejecuta la eliminación de una categoría"""
        # Obtener la categoría
        categoria = Categoria.objects.get(id=data.get("id"))
        nombre = categoria.nombre
        
        # Verificar si tiene materiales asociados
        if categoria.materiales.exists():
            # No eliminar, solo desactivar
            categoria.desactivar()
            return {
                "success": True, 
                "message": f"Categoría '{nombre}' desactivada (tiene materiales asociados)",
                "action": "deactivated"
            }
        else:
            # Eliminar completamente
            categoria.delete()
            return {
                "success": True, 
                "message": f"Categoría '{nombre}' eliminada permanentemente",
                "action": "deleted"
            }
    
    def execute_rem_mat(self, data):
        """Ejecuta la eliminación de un material"""
        # Obtener el material
        material = Material.objects.get(codigo=data.get("codigo"))
        nombre = material.nombre
        
        # Verificar si tiene ventas asociadas
        if material.ventas.exists():
            # No se puede eliminar, está asociado a datos históricos
            return {
                "success": False, 
                "error": f"No se puede eliminar el material '{nombre}' porque tiene ventas asociadas"
            }
        else:
            # Eliminar completamente
            material.delete()
            return {
                "success": True, 
                "message": f"Material '{nombre}' eliminado permanentemente",
                "action": "deleted"
            }
    
    def execute_get_mat(self, data):
        """Ejecuta la obtención de información de un material"""
        material = Material.objects.get(codigo=data.get("codigo"))
        return {
            "success": True,
            "object": {
                "codigo": material.codigo,
                "nombre": material.nombre,
                "descripcion": material.descripcion,
                "precio_compra": float(material.precio_compra),
                "precio_venta": float(material.precio_venta),
                "stock": material.stock,
                "stock_minimo": material.stock_minimo,
                "categoria": {
                    "id": material.categoria.id,
                    "nombre": material.categoria.nombre
                },
                "proveedor": {
                    "id": material.proveedor.id_proveedor,
                    "nombre": material.proveedor.nombre
                },
                "unidad": {
                    "id": material.unidad.id,
                    "nombre": material.unidad.nombre,
                    "abreviacion": material.unidad.abreviacion
                }
            }
        }
    
    def execute_list_mat(self, data):
        """Ejecuta el listado de materiales"""
        # Obtener lista de materiales (con posibles filtros)
        materials = Material.objects.all()
        
        # Aplicar filtros si existen en data
        if "categoria_id" in data:
            materials = materials.filter(categoria_id=data.get("categoria_id"))
        if "stock_bajo" in data and data.get("stock_bajo"):
            materials = materials.filter(stock__lt=F('stock_minimo'))

        
        # Limitar cantidad si es necesario
        limit = data.get("limit", 100)
        materials = materials[:limit]
        
        # Formatear resultados
        result_list = []
        for mat in materials:
            result_list.append({
                "codigo": mat.codigo,
                "nombre": mat.nombre,
                "precio_venta": float(mat.precio_venta),
                "stock": mat.stock,
                "categoria": mat.categoria.nombre
            })
        
        return {
            "success": True,
            "count": len(result_list),
            "objects": result_list
        }
    
    # Los demás métodos de ejecución para las diferentes combinaciones
    # ...