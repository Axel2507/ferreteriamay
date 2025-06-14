from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from inventario.models import Material, Categoria, Proveedor, Unidad, Venta, Devolucion, Descuento
from inventario.models.venta import DetalleVenta
import re 

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data
        self.command = parsed_data.get("command")
        self.entity = parsed_data.get("entity")
        self.data = parsed_data.get("data", {})
    
    def analyze(self):
        """Realiza el análisis semántico según el comando y la entidad"""
        method_name = f"analyze_{self.command.lower()}_{self.entity.lower()}"
        if hasattr(self, method_name):
            analyzer_method = getattr(self, method_name)
            return analyzer_method()
        else:
            raise SemanticError(f"No existe un analizador semántico para {self.command} {self.entity}")
    
    def analyze_add_mat(self):
        """Analiza semánticamente la adición de un material"""
        
        # Verificar que el nombre no esté duplicado
        if Material.objects.filter(nombre=self.data.get("nombre")).exists():
            raise SemanticError(f"Ya existe un material con el nombre '{self.data.get('nombre')}'")
        
        # Verificar que la categoría existe
        try:
            categoria = Categoria.objects.get(id=self.data.get("categoria_id"))
            if not categoria.activa:
                raise SemanticError(f"La categoría con ID {self.data.get('categoria_id')} está inactiva")
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe una categoría con ID {self.data.get('categoria_id')}")
        
        # Verificar que el proveedor existe y está activo
        try:
            proveedor = Proveedor.objects.get(id_proveedor=self.data.get("proveedor_id"))
            if not proveedor.activo:
                raise SemanticError(f"El proveedor con ID {self.data.get('proveedor_id')} está inactivo")
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe un proveedor con ID {self.data.get('proveedor_id')}")
        # Verificar precios válidos
        if self.data.get("precio_compra") <= 0:
            raise SemanticError("El precio de compra debe ser mayor que cero")
        
        if self.data.get("precio_venta") <= 0:
            raise SemanticError("El precio de venta debe ser mayor que cero")
        
        if self.data.get("precio_venta") <= self.data.get("precio_compra"):
            raise SemanticError("El precio de venta debe ser mayor que el precio de compra")
        
        # Verificar stock válido
        if self.data.get("stock_minimo") < 0:
            raise SemanticError("El stock mínimo no puede ser negativo")
        
        # Verificar unidad de compra
        try:
            Unidad.objects.get(id=self.data.get("unidad_compra_id"))
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe una unidad de compra con ID {self.data.get('unidad_compra_id')}")

        # Verificar unidad de venta
        try:
            Unidad.objects.get(id=self.data.get("unidad_venta_id"))
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe una unidad de venta con ID {self.data.get('unidad_venta_id')}")

        
        # Todo está bien, el comando es semánticamente válido
        return True
    
    def analyze_add_cat(self):
        """Analiza semánticamente la adición de una categoría"""
        # Verificar que el nombre no esté duplicado
        if Categoria.objects.filter(nombre=self.data.get("nombre")).exists():
            raise SemanticError(f"Ya existe una categoría con el nombre '{self.data.get('nombre')}'")
        if Categoria.objects.filter(abreviacion=self.data.get("abreviacion")).exists():
            raise SemanticError(f"Ya existe una categoría con la abreviacion '{self.data.get('abreviacion')}'")
        # Todo está bien, el comando es semánticamente válido
        return True
    
    def analyze_add_ven(self):
        """Analiza semánticamente la adición de una venta"""
        # Verificar que el total sea positivo
        if self.data.get("total") <= 0:
            raise SemanticError("El total de la venta debe ser mayor que cero")
        
        # Se necesitaría detalle de venta para más validaciones
        # Aquí se puede verificar existencia de productos, stock disponible, etc.
        # Todo está bien, el comando es semánticamente válido
        return True
    
    def analyze_add_dev(self):
        """Analiza semánticamente la adición de una devolución"""
        # Verificar que la venta exista
        try:
            venta = Venta.objects.get(id=self.data.get("venta_id"))
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe una venta con ID {self.data.get('venta_id')}")
        
        # Verificar que la venta no tenga devolución ya procesada
        if Devolucion.objects.filter(venta=venta, estado='procesada').exists():
            raise SemanticError(f"La venta con ID {self.data.get('venta_id')} ya tiene una devolución procesada")
        
        # Todo está bien, el comando es semánticamente válido
        return True
    
    def analyze_act_mat(self):
        """Analiza semánticamente la actualización de un material"""
        # Verificar que el material exista
        try:
            material = Material.objects.get(codigo=self.data.get("codigo"))
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe un material con el código '{self.data.get('codigo')}'")
        
        # Verificar que el nuevo nombre no esté duplicado (si se cambia)
        if self.data.get("nombre") != material.nombre and Material.objects.filter(nombre=self.data.get("nombre")).exists():
            raise SemanticError(f"Ya existe un material con el nombre '{self.data.get('nombre')}'")
        
        # Verificar que la categoría existe
        if "categoria_id" in self.data:
            try:
                categoria = Categoria.objects.get(id=self.data.get("categoria_id"))
                if not categoria.activa:
                    raise SemanticError(f"La categoría con ID {self.data.get('categoria_id')} está inactiva")
            except ObjectDoesNotExist:
                raise SemanticError(f"No existe una categoría con ID {self.data.get('categoria_id')}")
        
        # Verificar que el proveedor existe y está activo
        if "proveedor_id" in self.data:
            try:
                proveedor = Proveedor.objects.get(id_proveedor=self.data.get("proveedor_id"))
                if not proveedor.activo:
                    raise SemanticError(f"El proveedor con ID {self.data.get('proveedor_id')} está inactivo")
            except ObjectDoesNotExist:
                raise SemanticError(f"No existe un proveedor con ID {self.data.get('proveedor_id')}")
        
        # Verificar que la unidad existe
        if "unidad_id" in self.data:
            try:
                Unidad.objects.get(id=self.data.get("unidad_id"))
            except ObjectDoesNotExist:
                raise SemanticError(f"No existe una unidad con ID {self.data.get('unidad_id')}")
        
        # Verificar precios válidos
        if "precio_compra" in self.data and self.data.get("precio_compra") <= 0:
            raise SemanticError("El precio de compra debe ser mayor que cero")
        
        if "precio_venta" in self.data and self.data.get("precio_venta") <= 0:
            raise SemanticError("El precio de venta debe ser mayor que cero")
        
        if "precio_compra" in self.data and "precio_venta" in self.data:
            if self.data.get("precio_venta") <= self.data.get("precio_compra"):
                raise SemanticError("El precio de venta debe ser mayor que el precio de compra")
        elif "precio_compra" in self.data:
            if self.data.get("precio_compra") >= material.precio_venta:
                raise SemanticError("El nuevo precio de compra debe ser menor que el precio de venta actual")
        elif "precio_venta" in self.data:
            if self.data.get("precio_venta") <= material.precio_compra:
                raise SemanticError("El nuevo precio de venta debe ser mayor que el precio de compra actual")
        
        # Verificar stock válido
        if "stock_minimo" in self.data and self.data.get("stock_minimo") < 0:
            raise SemanticError("El stock mínimo no puede ser negativo")
        
        # Todo está bien, el comando es semánticamente válido
        return True
    
    def analyze_act_cat(self):
        """Analiza semánticamente la actualización de una categoría y la aplica"""
        # Verificar que la categoría exista
        try:
            categoria = Categoria.objects.get(id=self.data.get("id"))
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe una categoría con ID {self.data.get('id')}")

        # Verificar si se desea cambiar el nombre y si está duplicado
        nuevo_nombre = self.data.get("nombre")
        if nuevo_nombre and nuevo_nombre != categoria.nombre:
            if Categoria.objects.filter(nombre=nuevo_nombre).exclude(id=categoria.id).exists():
                raise SemanticError(f"Ya existe una categoría con el nombre '{nuevo_nombre}'")

        # Verificar si se desea cambiar la abreviación y si está duplicada
        nueva_abreviacion = self.data.get("abreviacion")
        if nueva_abreviacion and nueva_abreviacion != categoria.abreviacion:
            if Categoria.objects.filter(abreviacion=nueva_abreviacion).exclude(id=categoria.id).exists():
                raise SemanticError(f"Ya existe una categoría con la abreviación '{nueva_abreviacion}'")

        # ✅ ACTUALIZAR LOS VALORES Y GUARDAR
        categoria.nombre = nuevo_nombre
        categoria.abreviacion = nueva_abreviacion
        categoria.save()

        return True
     
    def analyze_add_prov(self):
        """Analiza semánticamente la adición de una categoría"""
        # Verificar que el nombre no esté duplicado
        if Proveedor.objects.filter(correo=self.data.get("email")).exists():
            raise SemanticError(f"Ya existe un correo con  '{self.data.get('email')}'")
        if Proveedor.objects.filter(telefono=self.data.get("telefono")).exists():
            raise SemanticError(f"Ya existe un telefono con el numero '{self.data.get('telefono')}'")
        # Todo está bien, el comando es semánticamente válido
        return True
    
    def analyze_add_uni(self):
        """Analiza semánticamente la adición de una unidad"""
        # Verificar que el nombre no esté duplicado
        if Unidad.objects.filter(nombre=self.data.get("nombre")).exists():
            raise SemanticError(f"Ya existe una unidad con el nombre '{self.data.get('nombre')}'")
        
        # Verificar que la abreviación no esté duplicada
        if Unidad.objects.filter(abreviacion=self.data.get("abreviacion")).exists():
            raise SemanticError(f"Ya existe una unidad con la abreviación '{self.data.get('abreviacion')}'")
        
        # Todo bien
        return True
    
    def analyze_add_dven(self):
        """
        Valida que haya suficiente stock para la venta de un material
        """
        cantidad = self.data.get("cantidad")
        codigo = self.data.get("codigo")
        try:
            material = Material.objects.get(codigo=codigo)
        except Material.DoesNotExist:
            raise SemanticError(f"El material con código '{codigo}' no existe")

        if material.stock < cantidad:
            raise SemanticError(
                f"No hay suficiente stock para el material '{material.nombre}'.\n"
                f"Stock disponible: {material.stock}, solicitado: {cantidad}"
            )

        return True
    # Más métodos para cada combinación de comando y entidad
    # ...
    def analyze_rem_mat(self):
        """Analiza semánticamente la eliminación de un material"""

        codigo = self.data.get("codigo")
        
        # Verificar que el material exista
        try:
            material = Material.objects.get(codigo=codigo)
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe un material con el código '{codigo}'")
        
        # Todo está bien
        return True
    
    def analyze_act_prov(self):
        """Analiza semánticamente la actualización de un proveedor"""

        # Verificar que el proveedor exista
        try:
            proveedor = Proveedor.objects.get(id_proveedor=self.data.get("id"))
        except ObjectDoesNotExist:
            raise SemanticError(f"No existe un proveedor con ID '{self.data.get('id')}'")

        # Verificar que el nuevo nombre de empresa no esté duplicado (si se cambia)
        nuevo_nombre = self.data.get("nombre_empresa")
        if nuevo_nombre != proveedor.nombre_empresa and Proveedor.objects.filter(nombre_empresa=nuevo_nombre).exists():
            raise SemanticError(f"Ya existe un proveedor con el nombre de empresa '{nuevo_nombre}'")

        # Verificar formato básico del teléfono (opcional, puedes ajustar la validación)
        telefono = self.data.get("telefono")
        if telefono and not re.fullmatch(r"\(\d{3}\)\d{3}-\d{4}", telefono):
           raise SemanticError("El número de teléfono debe tener el formato (###)###-####")

        # Verificar que el correo no esté repetido (si se cambia)
        nuevo_correo = self.data.get("correo")
        if nuevo_correo != proveedor.correo and Proveedor.objects.filter(correo=nuevo_correo).exists():
            raise SemanticError(f"Ya existe un proveedor con el correo '{nuevo_correo}'")

        # Verificar formato básico del correo (muy básico)
        if "@" not in nuevo_correo or "." not in nuevo_correo:
            raise SemanticError("El correo electrónico no tiene un formato válido")

        # Verificar que no se dejen campos esenciales vacíos
        campos_obligatorios = ["nombre_empresa", "nombre_contacto", "telefono", "correo", "direccion"]
        for campo in campos_obligatorios:
            valor = self.data.get(campo)
            if valor is None or str(valor).strip() == "":
                raise SemanticError(f"El campo '{campo}' no puede estar vacío")

        # Todo está bien
        return True
