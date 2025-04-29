import re
from datetime import datetime

class LexerError(Exception):
    pass

class Lexer:
    token_patterns = {
        # Comandos básicos
        "ADD": r"^ADD\b",
        "ACT": r"^ACT\b",
        "REM": r"^REM\b",
        # Entidades
        "MAT": r"^MAT\b",
        "VEN": r"^VEN\b",
        "DVEN": r"^DVEN\b",
        "DEV": r"^DEV\b",
        "DDEV": r"^DDEV\b",
        "CAT": r"^CAT\b",
        "PROV": r"^PROV\b",
        "UNI": r"^UNI\b",
        "DESC": r"^DESC\b",
        
        # Tokens específicos
        "Abreviacion": r"^[A-Z]{3}\b",
        "Precio": r"^\$?\d+\.\d{2}\b",
        "ID": r"^I[0-9]+\b",
        "Telefono": r"^\(\d{2,3}\)\s\d{4,5}-\d{4}",
        "Email": r"^[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]{0,63}[a-zA-Z0-9])?@(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}\b",
        "CODIGO": r"^C[0-9_-]{1,50}\b",
        "Nombre": r'^"[^"]*"',
        "Cantidad": r"^[0-9]+\b",
        "Porcentaje": r"^[0-9]+(\.[0-9]{1,2})?\%\b",
        "Fecha": r"^\d{2}/\d{2}/\d{4}\b",
        "Boolean": r"^(true|false|True|False|1|0)\b",
        "NULL": r"^NULL\b"
    }

    command_structures = {
        # Materiales
        "ADD_MAT": (
            ["ADD", "MAT", "CODIGO", "Nombre", "Precio", "Precio", "Cantidad", "Cantidad", "ID", "ID", "ID", "ID", "Cantidad" , "Fecha"],
            'ADD MAT CODIGO "Nombre del Material" $10.50 $15.75 100 10 I1 I2 I3 I4 12 01/01/2026'
        ),
        "ACT_MAT": (
            ["ACT", "MAT", "CODIGO", "Nombre", "Precio", "Precio", "Cantidad", "Cantidad", "ID", "ID", "ID", "ID", "Cantidad" , "Fecha"],
            'ACT MAT CODIGO "Nombre del Material" $10.50 $15.75 100 10 I1 I2 I3 I4 12 01/01/2026'
        ),
        "REM_MAT": (["REM", "MAT", "CODIGO"], 'REM MAT C123001'),
        
        # Categorías
        "ADD_CAT": (["ADD", "CAT", "Nombre", "Abreviacion"], 'ADD CAT "Herramientas" "HTM"'),
        "ACT_CAT": (["ACT", "CAT", "ID", "Nombre", "Abreviacion"], 'ACT CAT I1 "Herramientas" "HTM"'),
        "REM_CAT": (["REM", "CAT", "ID"], 'REM CAT I1'),
        
        # Proveedores
        "ADD_PROV": (
            ["ADD", "PROV", "Nombre", "Nombre", "Telefono", "Email", "Nombre"],
            'ADD PROV "Nombre Empresa" "Nombre Contacto" +1234567890 correo@ejemplo.com \'Dirección\''
        ),
        "ACT_PROV": (
            ["ACT", "PROV", "ID", "Nombre", "Nombre", "Telefono", "Email", "Nombre"],
            'ACT PROV I1 "Nombre Empresa" "Nombre Contacto" +1234567890 correo@ejemplo.com \'Dirección\''
        ),
        "REM_PROV": (["REM", "PROV", "ID"], 'REM PROV I1'),
        
        # Unidades
        "ADD_UNI": (["ADD", "UNI", "Nombre", "Abreviacion"], 'ADD UNI "Kilogramos" KG'),
        "ACT_UNI": (["ACT", "UNI", "ID", "Nombre", "Abreviacion"], 'ACT UNI I1 "Kilogramos" KG'),
        "REM_UNI": (["REM", "UNI", "ID"], 'REM UNI I1'),
        
        # Ventas
        "ADD_VEN": (["ADD", "VEN", "Precio"], 'ADD VEN $100.50'),
        "REM_VEN": (["REM", "VEN", "ID"], 'REM VEN I1'),

        #Detalle venta
        "ADD_DVEN": (
        ["ADD", "DVEN", "VentaID", "CodigoMaterial", "Cantidad", "Subtotal"],
        'ADD DVEN I5 C1234567890123 3 45.00'),
        
        # Devoluciones
        "ADD_DEV": (["ADD", "DEV", "ID", "Nombre", "Fecha"], 'ADD DEV I1 \'Motivo de devolución\' 25/04/2025'),
        "ACT_DEV": (["ACT", "DEV", "ID", "Nombre", "Fecha"], 'ACT DEV I1 \'Nuevo motivo\' 25/04/2025'),
        
        #Detalle Devolucion
        "ADD_DDEV": (
        ["ADD", "DDEV", "DevolucionID", "DetalleVentaID", "CantidadDevuelta"],
        'ADD DDEV I3 I7 1'),
        # Descuentos
        "ADD_DESC": (
            ["ADD", "DESC", "Nombre", "Porcentaje", "Fecha", "Fecha", "Boolean", "CODIGO"],
            'ADD DESC "Descuento Temporada" 15% 01/05/2025 31/05/2025 true C123001'
        ),
        "ACT_DESC": (
            ["ACT", "DESC", "ID", "Nombre", "Porcentaje", "Fecha", "Fecha", "Boolean", "CODIGO"],
            'ACT DESC I1 "Descuento Temporada" 15% 01/05/2025 31/05/2025 true C123001'
        ),
        "REM_DESC": (["REM", "DESC", "ID"], 'REM DESC I1'),
    }

    def __init__(self, input_str: str):
        self.input = input_str.strip()
        self.tokens = []
        self.original_input = input_str

    def tokenize(self):
        self.tokens = []  # Reset tokens
        remaining_input = self.input
        
        while remaining_input:
            matched = False
            for name, pattern in self.token_patterns.items():
                match = re.match(pattern, remaining_input)
                if match:
                    value = match.group()
                    # Limpieza de comillas en strings
                    if name in ["Nombre", "Texto"]:
                        # Quitar las comillas/apóstrofes del valor
                        if name == "Nombre":
                            value = value[1:-1]  # Quitar comillas dobles
                        else:
                            value = value[1:-1]  # Quitar comillas simples
                    
                    # Limpieza de valores numéricos
                    if name == "Precio":
                        value = value.replace('$', '')
                    elif name == "Porcentaje":
                        value = value.replace('%', '')
                    
                    # Conversión de booleanos
                    if name == "Boolean":
                        value = value.lower() in ['true', '1']
                    
                    # Manejar NULL explícitamente
                    if name == "NULL":
                        value = None
                    
                    self.tokens.append((name, value))
                    remaining_input = remaining_input[match.end():].strip()
                    matched = True
                    break
               
            if not matched:
                invalid = remaining_input.split(" ")[0] if " " in remaining_input else remaining_input
                raise LexerError(f"Token inválido encontrado: '{invalid}' en la entrada: '{self.original_input}'")

            print("Tokens encontrados:")
            for token in self.tokens:
             print(token)
        return self.tokens

    def validate(self):
        if len(self.tokens) < 2:
            raise LexerError("Se esperaba un comando y subcomando mínimo")

        key = f"{self.tokens[0][0]}_{self.tokens[1][0]}"
        if key not in self.command_structures:
            raise LexerError(f"Comando no reconocido: {' '.join([t[1] for t in self.tokens[:2]])}")

        expected, example = self.command_structures[key]
        
        # Validar cantidad de tokens, permitiendo flexibilidad para valores NULL opcionales
        if len(self.tokens) < len(expected):
            raise LexerError(
                f"Cantidad de tokens insuficiente. Se esperaba {len(expected)}, recibidos {len(self.tokens)}.\n"
                f"Ejemplo: {example}"
            )
        
        # Validar tipo de token en cada posición
        for i, (token_name, token_value) in enumerate(self.tokens):
            if i >= len(expected):
                # Se permiten tokens adicionales en algunos casos
                continue
                
            if token_name != expected[i] and token_name != "NULL":
                raise LexerError(
                    f"Token inválido en posición {i + 1}. "
                    f"Esperado: {expected[i]} - Encontrado: {token_name} ('{token_value}')\n"
                    f"Ejemplo: {example}"
                )
        
        return True

    def analizar(self):
        self.tokenize()
        self.validate()
        return self.tokens
    
    def parse_date(self, date_str):
        """Convierte una cadena de fecha en un objeto datetime"""
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            raise LexerError(f"Formato de fecha inválido: {date_str}. Use DD/MM/YYYY")