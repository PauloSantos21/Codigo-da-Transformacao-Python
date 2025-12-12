"""
Testes automatizados para a classe Calculadora
Criado com pytest para validar todos os métodos da calculadora
"""

import pytest # type: ignore
import sys
from pathlib import Path

# Adicionar o caminho do módulo anterior ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "modulo_09"))

from divisao_por_zero_tratamento_erros import Calculadora # type: ignore


class TestCalculadora:
    """Classe de testes para a Calculadora"""
    
    @pytest.fixture
    def calculadora(self):
        """Fixture que cria uma instância da Calculadora para cada teste"""
        return Calculadora()
    
    # ==================== TESTES PARA SOMAR ====================
    
    def test_somar_inteiros_positivos(self, calculadora):
        """Testa soma de dois inteiros positivos"""
        resultado = calculadora.somar(5, 3)
        assert resultado == 8
    
    def test_somar_inteiros_negativos(self, calculadora):
        """Testa soma com números negativos"""
        resultado = calculadora.somar(-5, -3)
        assert resultado == -8
    
    def test_somar_numeros_mistos(self, calculadora):
        """Testa soma de números positivos e negativos"""
        resultado = calculadora.somar(10, -4)
        assert resultado == 6
    
    def test_somar_floats(self, calculadora):
        """Testa soma de números com decimais"""
        resultado = calculadora.somar(3.5, 2.5)
        assert resultado == 6.0
    
    def test_somar_zero(self, calculadora):
        """Testa soma com zero"""
        resultado = calculadora.somar(5, 0)
        assert resultado == 5
    
    def test_somar_tipos_invalidos(self, calculadora, capsys):
        """Testa soma com tipos de dados inválidos"""
        resultado = calculadora.somar("5", 3)
        assert resultado is None
        captured = capsys.readouterr()
        assert "ERRO" in captured.out
    
    # ==================== TESTES PARA DIVIDIR ====================
    
    def test_dividir_numeros_positivos(self, calculadora):
        """Testa divisão de dois números positivos"""
        resultado = calculadora.dividir(10, 2)
        assert resultado == 5
    
    def test_dividir_numeros_negativos(self, calculadora):
        """Testa divisão com números negativos"""
        resultado = calculadora.dividir(-10, 2)
        assert resultado == -5
    
    def test_dividir_floats(self, calculadora):
        """Testa divisão com números decimais"""
        resultado = calculadora.dividir(7.5, 2.5)
        assert resultado == 3.0
    
    def test_dividir_resultado_decimal(self, calculadora):
        """Testa divisão que resulta em número decimal"""
        resultado = calculadora.dividir(5, 2)
        assert resultado == 2.5
    
    def test_dividir_por_zero(self, calculadora, capsys):
        """Testa divisão por zero - deve retornar None"""
        resultado = calculadora.dividir(10, 0)
        assert resultado is None
        captured = capsys.readouterr()
        assert "ERRO" in captured.out
        assert "zero" in captured.out.lower()
    
    def test_dividir_tipos_invalidos(self, calculadora, capsys):
        """Testa divisão com tipos de dados inválidos"""
        resultado = calculadora.dividir("10", 2)
        assert resultado is None
        captured = capsys.readouterr()
        assert "ERRO" in captured.out
    
    def test_dividir_zero_por_numero(self, calculadora):
        """Testa divisão de zero por um número"""
        resultado = calculadora.dividir(0, 5)
        assert resultado == 0.0
    
    # ==================== TESTES PARA SUBTRAIR ====================
    
    def test_subtrair_inteiros(self, calculadora):
        """Testa subtração de dois inteiros"""
        resultado = calculadora.subtrair(10, 3)
        assert resultado == 7
    
    def test_subtrair_numeros_negativos(self, calculadora):
        """Testa subtração com números negativos"""
        resultado = calculadora.subtrair(-5, -3)
        assert resultado == -2
    
    def test_subtrair_floats(self, calculadora):
        """Testa subtração com decimais"""
        resultado = calculadora.subtrair(10.5, 2.3)
        assert abs(resultado - 8.2) < 0.01
    
    def test_subtrair_tipos_invalidos(self, calculadora, capsys):
        """Testa subtração com tipos inválidos"""
        resultado = calculadora.subtrair(10, "3")
        assert resultado is None
        captured = capsys.readouterr()
        assert "ERRO" in captured.out
    
    # ==================== TESTES PARA MULTIPLICAR ====================
    
    def test_multiplicar_inteiros(self, calculadora):
        """Testa multiplicação de dois inteiros"""
        resultado = calculadora.multiplicar(4, 5)
        assert resultado == 20
    
    def test_multiplicar_numeros_negativos(self, calculadora):
        """Testa multiplicação com números negativos"""
        resultado = calculadora.multiplicar(-4, 5)
        assert resultado == -20
    
    def test_multiplicar_floats(self, calculadora):
        """Testa multiplicação com decimais"""
        resultado = calculadora.multiplicar(2.5, 4.0)
        assert resultado == 10.0
    
    def test_multiplicar_por_zero(self, calculadora):
        """Testa multiplicação por zero"""
        resultado = calculadora.multiplicar(100, 0)
        assert resultado == 0
    
    def test_multiplicar_tipos_invalidos(self, calculadora, capsys):
        """Testa multiplicação com tipos inválidos"""
        # Em Python, string * número é válido (repetição), testando com None
        resultado = calculadora.multiplicar(5, None)
        assert resultado is None
        captured = capsys.readouterr()
        assert "ERRO" in captured.out
    
    # ==================== TESTES PARAMETRIZADOS ====================
    
    @pytest.mark.parametrize("a,b,esperado", [
        (2, 3, 5),
        (-2, -3, -5),
        (0, 0, 0),
        (100, -50, 50),
        (3.5, 2.5, 6.0),
    ])
    def test_somar_parametrizado(self, calculadora, a, b, esperado):
        """Testa somar com múltiplos conjuntos de dados"""
        resultado = calculadora.somar(a, b)
        assert resultado == esperado
    
    @pytest.mark.parametrize("a,b,esperado", [
        (10, 2, 5.0),
        (20, 4, 5.0),
        (-10, 2, -5.0),
        (7.5, 2.5, 3.0),
        (0, 5, 0.0),
    ])
    def test_dividir_parametrizado(self, calculadora, a, b, esperado):
        """Testa dividir com múltiplos conjuntos de dados"""
        resultado = calculadora.dividir(a, b)
        assert resultado == esperado
    
    # ==================== TESTES DE CASOS EXTREMOS ====================
    
    def test_operacoes_com_numeros_grandes(self, calculadora):
        """Testa operações com números muito grandes"""
        numero_grande = 10**10
        assert calculadora.somar(numero_grande, numero_grande) == numero_grande * 2
        assert calculadora.multiplicar(numero_grande, 2) == numero_grande * 2
    
    def test_operacoes_com_numeros_muito_pequenos(self, calculadora):
        """Testa operações com números muito pequenos"""
        numero_pequeno = 0.0001
        resultado = calculadora.somar(numero_pequeno, numero_pequeno)
        assert abs(resultado - 0.0002) < 1e-10


class TestCalculadoraIntegracao:
    """Testes de integração para operações combinadas"""
    @pytest.fixture
    def calculadora(self):
        """Fixture que cria uma instância da Calculadora"""
        return Calculadora()
    
    def test_sequencia_operacoes(self, calculadora):
        """Testa uma sequência de operações matemáticas"""
        # (10 + 5) = 15
        resultado1 = calculadora.somar(10, 5)
        assert resultado1 == 15
        
        # 15 * 2 = 30
        resultado2 = calculadora.multiplicar(resultado1, 2)
        assert resultado2 == 30
        
        # 30 / 3 = 10
        resultado3 = calculadora.dividir(resultado2, 3)
        assert resultado3 == 10
        
        # 10 - 5 = 5
        resultado4 = calculadora.subtrair(resultado3, 5)
        assert resultado4 == 5
    
    def test_calculo_media(self, calculadora):
        """Testa cálculo de média usando a calculadora"""
        # Somando valores
        soma = calculadora.somar(10, calculadora.somar(20, 30))
        # Dividindo pelo número de elementos (média)
        media = calculadora.dividir(soma, 3)
        assert media == 20.0
    
    def test_calculo_desconto(self, calculadora):
        """Testa cálculo de desconto (preço com 10% de desconto)"""
        preco_original = 100
        percentual_desconto = 10
        
        # Calcula o desconto: 100 * 0.10 = 10
        desconto = calculadora.multiplicar(preco_original, percentual_desconto)
        desconto = calculadora.dividir(desconto, 100)
        
        # Calcula o preço final: 100 - 10 = 90
        preco_final = calculadora.subtrair(preco_original, desconto)
        assert preco_final == 90.0


if __name__ == "__main__":
    # Executar os testes com relatório detalhado
    pytest.main([__file__, "-v", "--tb=short", "-ra"])