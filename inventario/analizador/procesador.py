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
           

            print("Resultado del parser:", parsed_data)

            # Aquí cuando tomas los valores:
            data = parsed_data["data"]

            print("Datos antes de convertir a int:", data)
            
            # 3. Análisis semántico
            semantic = SemanticAnalyzer(parsed_data)
            semantic.analyze()
            
            # 4. Ejecución del comando
            return self.execute_command(parsed_data)
        except Exception as e:
         print("Excepción atrapada:", e)  # <<< AGREGA ESTE PRINT
         raise e  # <-- Lanza otra vez para que Django te siga diciendo qué pasó    
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
        unidad_compra = Unidad.objects.get(id=data.get("unidad_compra_id"))
        unidad_venta = Unidad.objects.get(id=data.get("unidad_venta_id"))
        # Crear nuevo material
        material = Material(
            codigo=data.get("codigo"),
            nombre=data.get("nombre"),
            precio_compra=data.get("precio_compra"),
            precio_venta=data.get("precio_venta"),
            stock=data.get("stock", 0),
            stock_minimo=data.get("stock_minimo", 0),
            categoria=Categoria.objects.get(id=data.get("categoria_id")),
            proveedor=Proveedor.objects.get(id_proveedor=data.get("proveedor_id")),
            unidad_compra=Unidad.objects.get(id=data.get("unidad_compra_id")),
            unidad_venta=Unidad.objects.get(id=data.get("unidad_venta_id")),
            factor_conversion=data.get("factor_conversion"),
            fecha_caducidad=data.get("fecha_caducidad"),
            activo=True
        )
        material.save()
        return {
            "success": True,
            "message": f"Material '{material.nombre}' creado correctamente",
            "object": {
                "codigo": material.codigo,
                "nombre": material.nombre,
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
                    "nombre_empresa": material.proveedor.nombre_empresa
                },
                "unidad_compra": {
                    "id": material.unidad_compra.id,
                    "nombre": material.unidad_compra.nombre
                },
                "unidad_venta": {
                    "id": material.unidad_venta.id,
                    "nombre": material.unidad_venta.nombre
                },
                "factor_conversion": material.factor_conversion,
                "activo": material.activo
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
        categoria.save()
        return {
            "success": True,
            "message": f"Categoria '{categoria.nombre}' creado correctamente",
            "object": {
                "nombre": categoria.nombre,
                "abreviacion": categoria.abreviacion,
                "activa": categoria.activa
           }
    }

    def execute_add_prov(self, data):
        """Ejecuta la adición de un proveedor"""
        print("Datos recibidos para crear proveedor:", data)
        # Crear un proveedor
        proveedor = Proveedor(
            nombre_empresa=data.get("nombre_empresa"),
            nombre_contacto=data.get("nombre_contacto"),
            telefono=data.get("telefono"),
            correo=data.get("email"),
            direccion=data.get("direccion"),
            activo=data.get("activo", True)
        )
        proveedor.save()
        # Guardar y retornar éxito
        return {
            "success": True,
            "message": f"Proveedor '{proveedor.nombre_empresa}' creado correctamente",
            "object": {
                "nombre_empresa": proveedor.nombre_empresa,
                "nombre_contacto": proveedor.nombre_contacto,
                "telefono": proveedor.telefono,
                "correo": proveedor.correo,
                "direccion": proveedor.direccion,
                "activo": proveedor.activo
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
    
    def execute_rem_prov(self, data):
        proveedor = Proveedor.objects.get(id=data.get("id"))
        proveedor.activo = False
        proveedor.save()

        return {
            "success": True,
            "message": f"Proveedor '{proveedor.nombre_empresa}' desactivado correctamente",
            "object": {
                "id": proveedor.id,
                "nombre_empresa": proveedor.nombre_empresa,
                "nombre_contacto": proveedor.nombre_contacto,
                "telefono": proveedor.telefono,
                "correo": proveedor.correo,
                "direccion": proveedor.direccion,
                "activo": proveedor.activo
            }
        }

    def execute_add_uni(self, data):
        """Ejecuta la adición de una unidad"""
        unidad = Unidad(
            nombre=data.get("nombre"),
            abreviacion=data.get("abreviacion"),
            activo=True  # Siempre activa al crearse
        )
        unidad.save()

        return {
            "success": True,
            "message": f"Unidad '{unidad.nombre}' creada correctamente",
            "object":{
                "id":unidad.id,
                "nombre": unidad.nombre,
                "abreviacion": unidad.abreviacion,
                "activo" : unidad.activo
            }
        }
    # Los demás métodos de ejecución para las diferentes combinaciones
    # ...
    def execute_add_dven(self, data):
        """
        Ejecuta la adición de un detalle de venta (DVEN)
        """
        from inventario.models.venta import Venta
        from inventario.models.venta import DetalleVenta
        from inventario.models.material import Material

        try:
            # Obtener la venta asociada
            venta = Venta.objects.get(id=data.get("id_venta"))
            
            # Obtener el material asociado
            material = Material.objects.get(codigo=data.get("codigo"))
            
            # Validar y descontar stock
            cantidad = data.get("cantidad")
            if material.stock < cantidad:
                return {
                    "success": False,
                    "error": f"Stock insuficiente para el material '{material.nombre}'"
                }

            # Crear el detalle de venta
            detalle = DetalleVenta(
                venta=venta,
                material=material,
                cantidad=cantidad,
                subtotal=data.get("subtotal")
            )
            detalle.save()

            # Descontar del stock
            material.stock -= cantidad
            material.save()

            return {
                "success": True,
                "message": f"Detalle de venta agregado: {material.nombre} x{cantidad}",
                "object": {
                    "venta_id": venta.id,
                    "codigo_material": material.codigo,
                    "nombre_material": material.nombre,
                    "cantidad": cantidad,
                    "subtotal": data.get("subtotal")
                }
            }

        except Venta.DoesNotExist:
            return {
                "success": False,
                "error": f"La venta con ID {data.get('id_venta')} no existe"
            }
        except Material.DoesNotExist:
            return {
                "success": False,
                "error": f"El material con código {data.get('codigo_material')} no existe"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
