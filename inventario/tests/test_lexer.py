import unittest
from inventario.analizador.lexer import Lexer, LexerError

class TestLexer(unittest.TestCase):

    def test_comando_valido_add_mat(self):
        comando = 'ADD MAT "Tornillo" 10.00 12.00 1 1 1'
        lexer = Lexer(comando)
        tokens = lexer.tokenize()
        token_names = [token[0] for token in tokens]

        esperado = ['ADD', 'MAT', 'Nombre', 'Precio', 'Precio', 'ID', 'ID', 'ID']
        self.assertEqual(token_names, esperado)

    def test_comando_valido_add_cat(self):
        comando = 'ADD CAT "Herramientas" ABC'
        lexer = Lexer(comando)
        tokens = lexer.tokenize()
        token_names = [token[0] for token in tokens]

        esperado = ['ADD', 'CAT', 'Nombre', 'Abreviacion']
        self.assertEqual(token_names, esperado)

    def test_comando_invalido_token(self):
      comando = 'XYZ MAT "Clavo" 5.00 6.00 1 1 1'
      lexer = Lexer(comando)

      lexer.tokenize()  # Puede tokenizar sin error

      with self.assertRaises(LexerError):
        lexer.validate()  # Aquí sí debe lanzar error porque 'XYZ' no es un comando válido


    def test_comando_invalido_formato(self):
        comando = 'ADD MAT "Clavo" 5.00 6.00'
        lexer = Lexer(comando)
        lexer.tokenize()

        with self.assertRaises(LexerError):
            lexer.validate()

if __name__ == '__main__':
    unittest.main()
