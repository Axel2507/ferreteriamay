class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.command = None
        self.entity = None
        self.parsed_data = {}
    
    def parse(self):
        """Analiza la estructura sintáctica de los tokens"""
        if not self.tokens:
            raise SyntaxError("No hay tokens para analizar")
        
        # Identificar comando principal
        command_token, command_value = self.tokens[0]
        if command_token != "ADD" and command_token != "ACT" and command_token != "REM" and command_token != "GET" and command_token != "LIST":
            raise SyntaxError(f"Se esperaba un comando (ADD, ACT, REM, GET, LIST), encontrado: {command_value}")
        
        self.command = command_value
        self.position += 1
        
        # Identificar entidad
        if self.position >= len(self.tokens):
            raise SyntaxError("Se esperaba una entidad después del comando")
        
        entity_token, entity_value = self.tokens[self.position]
        if entity_token not in ["MAT", "CAT", "PROV", "UNI", "VEN", "DEV", "DESC"]:
            raise SyntaxError(f"Se esperaba una entidad válida, encontrado: {entity_value}")
        
        self.entity = entity_value
        self.position += 1
        
        # Analizador específico por comando y entidad
        method_name = f"parse_{self.command.lower()}_{self.entity.lower()}"
        if hasattr(self, method_name):
            parser_method = getattr(self, method_name)
            return parser_method()
        else:
            # Método general para comandos no implementados específicamente
            return self.parse_general()
    
    def parse_general(self):
        """Método general para comandos que no requieren análisis específico"""
        # Por ahora, simplemente retorna todos los tokens menos el comando y la entidad
        result = {
            "command": self.command,
            "entity": self.entity,
            "params": {}
        }
        
        # Añadir parámetros según corresponda
        for i in range(self.position, len(self.tokens)):
            token_type, token_value = self.tokens[i]
            result["params"][token_type] = token_value
        
        return result
    
    # Métodos específicos para cada comando + entidad
    
    def parse_add_mat(self):
        """Analiza el comando ADD MAT"""
        result = {
            "command": "ADD",
            "entity": "MAT",
            "data": {}
        }
        
        # Validar y extraer parámetros
        # Código
        if self.position < len(self.tokens):
            _, codigo = self.tokens[self.position]
            result["data"]["codigo"] = codigo
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un código para el material")
        
        # Nombre
        if self.position < len(self.tokens):
            _, nombre = self.tokens[self.position]
            result["data"]["nombre"] = nombre
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un nombre para el material")
        
        # Precio compra
        if self.position < len(self.tokens):
            _, precio_compra = self.tokens[self.position]
            result["data"]["precio_compra"] = float(precio_compra)
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un precio de compra")
        
        # Precio venta
        if self.position < len(self.tokens):
            _, precio_venta = self.tokens[self.position]
            result["data"]["precio_venta"] = float(precio_venta)
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un precio de venta")
        
        # Stock
        if self.position < len(self.tokens):
            _, stock = self.tokens[self.position]
            result["data"]["stock"] = int(stock)
            self.position += 1
        else:
            raise SyntaxError("Se esperaba una cantidad de stock")
        
        # Stock mínimo
        if self.position < len(self.tokens):
            _, stock_min = self.tokens[self.position]
            result["data"]["stock_minimo"] = int(stock_min)
            self.position += 1
        else:
            raise SyntaxError("Se esperaba una cantidad de stock mínimo")
        
        # Categoría ID
        if self.position < len(self.tokens):
            _, categoria_id = self.tokens[self.position]
            result["data"]["categoria_id"] = categoria_id
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un ID de categoría")
        
        # Proveedor ID
        if self.position < len(self.tokens):
            _, proveedor_id = self.tokens[self.position]
            result["data"]["proveedor_id"] = proveedor_id
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un ID de proveedor")
        
        # Unidad ID
        if self.position < len(self.tokens):
            _, unidad_id = self.tokens[self.position]
            result["data"]["unidad_id"] = unidad_id
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un ID de unidad")
        
        return result
    
    def parse_add_cat(self):
        """Analiza el comando ADD CAT"""
        result = {
            "command": "ADD",
            "entity": "CAT",
            "data": {}
        }
        
        # Nombre
        if self.position < len(self.tokens):
            _, nombre = self.tokens[self.position]
            result["data"]["nombre"] = nombre
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un nombre para la categoría")
        
        return result
    
    def parse_add_ven(self):
        """Analiza el comando ADD VEN"""
        result = {
            "command": "ADD",
            "entity": "VEN",
            "data": {}
        }
        
        # Total de la venta
        if self.position < len(self.tokens):
            _, total = self.tokens[self.position]
            result["data"]["total"] = float(total)
            self.position += 1
        else:
            raise SyntaxError("Se esperaba un total para la venta")
        
        return result
    
    # Más métodos para cada combinación de comando y entidad
    # ...