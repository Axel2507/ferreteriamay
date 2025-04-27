import unittest
from inventario.analizador.lexer import Lexer, LexerError
from inventario.analizador.parser import Parser, SyntaxError

class TestParser(unittest.TestCase):

    def test_comando_valido_add_mat(self):
        comando = 'ADD MAT C123456789012 "Tornillo" 10.00 12.00 100 10 I1 I2 I3'
        lexer = Lexer(comando)
        tokens = lexer.analizar()

        parser = Parser(tokens)
        self.assertTrue(parser.parse())

        parser = Parser(tokens)
        self.assertTrue(parser.parse())

    def test_comando_valido_add_cat(self):
        comando = 'ADD CAT "Herramientas" ABC'
        lexer = Lexer(comando)
        tokens = lexer.analizar()

        parser = Parser(tokens)
        self.assertTrue(parser.parse())

    def test_comando_invalido_orden_tokens(self):
        comando = 'ADD MAT C123456789012 10.00 "Tornillo" 12.00 100 10 1 2 3'
        lexer = Lexer(comando)
        tokens = lexer.analizar()

        parser = Parser(tokens)
        with self.assertRaises(SyntaxError):
            parser.parsear()

    def test_comando_invalido_cantidad_tokens(self):
        comando = 'ADD MAT C123456789012 "Tornillo" 10.00 12.00 100 10 1 2'
        lexer = Lexer(comando)
        tokens = lexer.analizar()

        parser = Parser(tokens)
        with self.assertRaises(SyntaxError):
            parser.parse()

if __name__ == '__main__':
    unittest.main()
