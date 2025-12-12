"""
Testes com unittest para a função soma
Utilizando o framework unittest padrão do Python para validar a função de soma
"""

import unittest
import sys
from pathlib import Path

# Adicionar o caminho do módulo anterior ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "modulo_07"))

from atividade1_crie_import_arquiv_modulos_pacotes import somar # type: ignore


class TestFuncaoSoma(unittest.TestCase):
    """Classe de testes para a função soma usando unittest"""
    
    def test_soma_inteiros_positivos(self):
        """Testa soma de dois inteiros positivos"""
        resultado = somar(2, 3)
        self.assertEqual(resultado, 5)
    
    def test_soma_inteiros_negativos(self):
        """Testa soma de dois inteiros negativos"""
        resultado = somar(-5, -3)
        self.assertEqual(resultado, -8)
    
    def test_soma_inteiros_mistos(self):
        """Testa soma com números positivos e negativos"""
        resultado = somar(10, -4)
        self.assertEqual(resultado, 6)
    
    def test_soma_com_zero(self):
        """Testa soma com zero"""
        resultado = somar(5, 0)
        self.assertEqual(resultado, 5)
        
        resultado = somar(0, 5)
        self.assertEqual(resultado, 5)
    
    def test_soma_zero_com_zero(self):
        """Testa soma de zero com zero"""
        resultado = somar(0, 0)
        self.assertEqual(resultado, 0)
    
    def test_soma_numeros_floats(self):
        """Testa soma com números decimais"""
        resultado = somar(3.5, 2.5)
        self.assertEqual(resultado, 6.0)
    
    def test_soma_float_positivo_negativo(self):
        """Testa soma de float positivo com negativo"""
        resultado = somar(10.5, -2.3)
        self.assertAlmostEqual(resultado, 8.2, places=1)
    
    def test_soma_numeros_muito_grandes(self):
        """Testa soma com números muito grandes"""
        numero_grande = 10**10
        resultado = somar(numero_grande, numero_grande)
        self.assertEqual(resultado, numero_grande * 2)
    
    def test_soma_numeros_muito_pequenos(self):
        """Testa soma com números muito pequenos"""
        numero_pequeno = 0.0001
        resultado = somar(numero_pequeno, numero_pequeno)
        self.assertAlmostEqual(resultado, 0.0002, places=5)
    
    def test_soma_retorna_numero(self):
        """Testa que o resultado é um número"""
        resultado = somar(2, 3)
        self.assertIsInstance(resultado, (int, float))
    
    def test_soma_comutativa(self):
        """Testa propriedade comutativa: a + b = b + a"""
        a, b = 7, 12
        resultado1 = somar(a, b)
        resultado2 = somar(b, a)
        self.assertEqual(resultado1, resultado2)
    
    def test_soma_associativa(self):
        """Testa propriedade associativa: (a + b) + c = a + (b + c)"""
        a, b, c = 2, 3, 4
        resultado1 = somar(somar(a, b), c)
        resultado2 = somar(a, somar(b, c))
        self.assertEqual(resultado1, resultado2)
    
    def test_soma_identidade_aditiva(self):
        """Testa elemento neutro da soma: a + 0 = a"""
        numero = 42
        resultado = somar(numero, 0)
        self.assertEqual(resultado, numero)
    
    def test_soma_inverso_aditivo(self):
        """Testa inverso aditivo: a + (-a) = 0"""
        numero = 15
        resultado = somar(numero, -numero)
        self.assertEqual(resultado, 0)
    
    def test_soma_com_strings_concatena(self):
        """Testa que a soma com strings funciona como concatenação"""
        resultado = somar("2", "3")
        self.assertEqual(resultado, "23")
        self.assertIsInstance(resultado, str)
    
    def test_soma_numero_e_string_deveria_falhar(self):
        """Testa que a soma de número e string falha (TypeError)"""
        with self.assertRaises(TypeError):
            somar(2, "3")
    
    def test_soma_com_none_deveria_falhar(self):
        """Testa que a soma com None falha (TypeError)"""
        with self.assertRaises(TypeError):
            somar(None, 5)
    
    def test_soma_com_lista_deveria_funcionar(self):
        """Testa que a soma funciona com listas (concatenação)"""
        resultado = somar([1, 2], [3, 4])
        self.assertEqual(resultado, [1, 2, 3, 4])
    
    def test_soma_resultado_exato(self):
        """Testa que o resultado é exatamente igual"""
        self.assertEqual(somar(10, 20), 30)
        self.assertNotEqual(somar(10, 20), 31)
    
    def test_soma_multiplas_operacoes(self):
        """Testa sequência de somas"""
        resultado = somar(somar(somar(1, 2), 3), 4)
        self.assertEqual(resultado, 10)


class TestFuncaoSomaComParametros(unittest.TestCase):
    """Testes parametrizados para a função soma"""
    
    def test_multiplas_somas(self):
        """Testa múltiplos casos de soma"""
        casos_teste = [
            (1, 1, 2),
            (2, 3, 5),
            (-1, 1, 0),
            (10, -5, 5),
            (3.5, 1.5, 5.0),
            (100, 200, 300),
            (-10, -20, -30),
            (0, 100, 100),
        ]
        
        for a, b, esperado in casos_teste:
            with self.subTest(a=a, b=b):
                resultado = somar(a, b)
                self.assertEqual(resultado, esperado)


class TestFuncaoSomaEdgeCases(unittest.TestCase):
    """Testes de casos extremos para a função soma"""
    
    def test_soma_numeros_negativos_muito_grandes(self):
        """Testa soma com números negativos muito grandes"""
        numero_negativo_grande = -(10**10)
        resultado = somar(numero_negativo_grande, numero_negativo_grande)
        self.assertEqual(resultado, numero_negativo_grande * 2)
    
    def test_soma_com_infinito(self):
        """Testa soma com infinito"""
        infinito = float('inf')
        resultado = somar(infinito, 1)
        self.assertEqual(resultado, infinito)
    
    def test_soma_numeros_proximos_overflow(self):
        """Testa soma de números que se aproximam do limite"""
        numero_grande = 10**308
        # Python lida bem com números grandes, então não há overflow real
        resultado = somar(numero_grande, numero_grande)
        self.assertEqual(resultado, numero_grande * 2)
    
    def test_soma_com_valores_iguais(self):
        """Testa soma de valores iguais (resultado deve ser o dobro)"""
        numero = 42
        resultado = somar(numero, numero)
        self.assertEqual(resultado, numero * 2)


class TestFuncaoSomaComAssertions(unittest.TestCase):
    """Testes usando diferentes tipos de assertions"""
    
    def test_assertion_equal(self):
        """Testa assertEqual"""
        self.assertEqual(somar(2, 2), 4)
    
    def test_assertion_not_equal(self):
        """Testa assertNotEqual"""
        self.assertNotEqual(somar(2, 3), 4)
    
    def test_assertion_true(self):
        """Testa assertTrue"""
        resultado = somar(2, 3)
        self.assertTrue(resultado > 0)
    
    def test_assertion_false(self):
        """Testa assertFalse"""
        resultado = somar(-2, -3)
        self.assertFalse(resultado > 0)
    
    def test_assertion_is_none(self):
        """Testa assertIsNone (resultado não deve ser None)"""
        resultado = somar(1, 1)
        self.assertIsNotNone(resultado)
    
    def test_assertion_greater_than(self):
        """Testa assertGreater"""
        self.assertGreater(somar(10, 5), 10)
    
    def test_assertion_less_than(self):
        """Testa assertLess"""
        self.assertLess(somar(-10, 5), 0)
    
    def test_assertion_greater_equal(self):
        """Testa assertGreaterEqual"""
        self.assertGreaterEqual(somar(5, 5), 10)
    
    def test_assertion_in(self):
        """Testa assertIn"""
        resultado = somar(2, 3)
        self.assertIn(resultado, [4, 5, 6])


class TestFuncaoSomaIntegracao(unittest.TestCase):
    """Testes de integração da função soma"""
    
    def setUp(self):
        """Executado antes de cada teste"""
        self.soma_sucessos = 0
        self.soma_testes = 0
    
    def tearDown(self):
        """Executado após cada teste"""
        self.soma_testes += 1
    
    def test_calcular_soma_sequencial(self):
        """Testa cálculo seqüencial de somas"""
        valores = [1, 2, 3, 4, 5]
        resultado_final = 0
        
        for valor in valores:
            resultado_final = somar(resultado_final, valor)
            self.soma_sucessos += 1
        
        self.assertEqual(resultado_final, 15)
        self.assertEqual(self.soma_sucessos, 5)
    
    def test_soma_em_loop(self):
        """Testa soma em um loop"""
        total = 0
        for i in range(1, 6):
            total = somar(total, i)
        
        self.assertEqual(total, 15)
    
    def test_soma_com_condicional(self):
        """Testa soma com condicional"""
        resultado = somar(10, 5)
        
        if resultado == 15:
            self.soma_sucessos += 1
        
        self.assertEqual(self.soma_sucessos, 1)
    
    def test_comparacao_resultados(self):
        """Testa comparação entre diferentes somas"""
        soma1 = somar(10, 20)
        soma2 = somar(15, 15)
        
        self.assertEqual(soma1, soma2)


if __name__ == '__main__':
    # Executar os testes com verbosidade
    unittest.main(verbosity=2)