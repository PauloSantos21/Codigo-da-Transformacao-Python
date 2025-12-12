"""
Testes de validação de entradas inválidas
Verifica como o programa reage a entradas inválidas usando pytest
"""

import pytest # type: ignore
import sys
from pathlib import Path

# Adicionar o caminho do módulo anterior ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "modulo_09"))

from valide_entrada_usuario_tratamento_erros import ( # type: ignore
    validar_inteiro,
    validar_float,
    validar_idade,
    validar_texto,
    validar_email,
    validar_telefone,
    validar_cpf,
    validar_opcao
)


class TestValidarInteiro:
    """Testes para validação de números inteiros"""
    
    def test_inteiro_valido(self):
        """Testa entrada válida de inteiro"""
        assert validar_inteiro("42") == 42
        assert validar_inteiro("-10") == -10
        assert validar_inteiro("0") == 0
    
    def test_inteiro_invalido_string(self, capsys):
        """Testa entrada inválida com string não numérica"""
        resultado = validar_inteiro("abc")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_inteiro_invalido_float(self, capsys):
        """Testa entrada de número decimal para inteiro"""
        resultado = validar_inteiro("3.14")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_inteiro_invalido_vazio(self, capsys):
        """Testa entrada vazia"""
        resultado = validar_inteiro("")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_inteiro_com_minimo(self):
        """Testa validação com valor mínimo"""
        assert validar_inteiro("10", minimo=5) == 10
        assert validar_inteiro("4", minimo=5) is None
    
    def test_inteiro_com_maximo(self):
        """Testa validação com valor máximo"""
        assert validar_inteiro("10", maximo=20) == 10
        assert validar_inteiro("25", maximo=20) is None
    
    def test_inteiro_com_intervalo(self):
        """Testa validação dentro de intervalo"""
        assert validar_inteiro("15", minimo=10, maximo=20) == 15
        assert validar_inteiro("5", minimo=10, maximo=20) is None
        assert validar_inteiro("25", minimo=10, maximo=20) is None
    
    def test_inteiro_com_espacos(self):
        """Testa inteiro com espaços em branco"""
        assert validar_inteiro("  42  ") == 42


class TestValidarFloat:
    """Testes para validação de números decimais"""
    
    def test_float_valido(self):
        """Testa entrada válida de float"""
        assert validar_float("3.14") == 3.14
        assert validar_float("-2.5") == -2.5
        assert validar_float("0.0") == 0.0
    
    def test_float_inteiro(self):
        """Testa float aceitar inteiros"""
        assert validar_float("42") == 42.0
    
    def test_float_invalido_string(self, capsys):
        """Testa entrada inválida com string"""
        resultado = validar_float("abc")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_float_invalido_multiplos_pontos(self, capsys):
        """Testa entrada com múltiplos pontos decimais"""
        resultado = validar_float("3.14.15")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_float_com_minimo(self):
        """Testa validação float com valor mínimo"""
        assert validar_float("5.5", minimo=5.0) == 5.5
        assert validar_float("4.9", minimo=5.0) is None
    
    def test_float_com_maximo(self):
        """Testa validação float com valor máximo"""
        assert validar_float("5.5", maximo=6.0) == 5.5
        assert validar_float("6.5", maximo=6.0) is None


class TestValidarIdade:
    """Testes para validação de idade"""
    
    def test_idade_valida(self):
        """Testa idade válida"""
        assert validar_idade("25") == 25
        assert validar_idade("65") == 65
    
    def test_idade_zero(self):
        """Testa idade zero (válida)"""
        assert validar_idade("0") == 0
    
    def test_idade_negativa(self, capsys):
        """Testa idade negativa (inválida)"""
        resultado = validar_idade("-5")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_idade_muito_alta(self, capsys):
        """Testa idade acima do máximo (150)"""
        resultado = validar_idade("151")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_idade_maxima_permitida(self):
        """Testa idade máxima permitida (150)"""
        assert validar_idade("150") == 150
    
    def test_idade_invalida_string(self, capsys):
        """Testa entrada não numérica para idade"""
        resultado = validar_idade("abc")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_idade_menor_idade(self, capsys):
        """Testa aviso para menor de idade"""
        resultado = validar_idade("17")
        assert resultado == 17
        captured = capsys.readouterr()
        assert "Aviso" in captured.out or "menor" in captured.out.lower()


class TestValidarTexto:
    """Testes para validação de texto"""
    
    def test_texto_valido(self):
        """Testa texto válido"""
        assert validar_texto("Olá") == "Olá"
        assert validar_texto("João Silva") == "João Silva"
    
    def test_texto_vazio(self, capsys):
        """Testa texto vazio (inválido)"""
        resultado = validar_texto("")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_texto_so_espacos(self, capsys):
        """Testa texto contendo apenas espaços"""
        resultado = validar_texto("   ")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_texto_minimo_caracteres(self):
        """Testa validação de mínimo de caracteres"""
        assert validar_texto("ab", minimo_caracteres=2) == "ab"
        assert validar_texto("a", minimo_caracteres=2) is None
    
    def test_texto_maximo_caracteres(self):
        """Testa validação de máximo de caracteres"""
        assert validar_texto("abc", maximo_caracteres=5) == "abc"
        assert validar_texto("abcdef", maximo_caracteres=5) is None
    
    def test_texto_intervalo_caracteres(self):
        """Testa texto dentro de intervalo de caracteres"""
        assert validar_texto("abc", minimo_caracteres=2, maximo_caracteres=5) == "abc"
        assert validar_texto("a", minimo_caracteres=2, maximo_caracteres=5) is None
        assert validar_texto("abcdef", minimo_caracteres=2, maximo_caracteres=5) is None
    
    def test_texto_com_espacos_trim(self):
        """Testa que espaços extras são removidos"""
        assert validar_texto("  Olá  ") == "Olá"


class TestValidarEmail:
    """Testes para validação de email"""
    
    def test_email_valido(self):
        """Testa emails válidos"""
        assert validar_email("usuario@example.com") == "usuario@example.com"
        assert validar_email("joao.silva@empresa.com.br") == "joao.silva@empresa.com.br"
        assert validar_email("test+tag@example.co.uk") == "test+tag@example.co.uk"
    
    def test_email_sem_arroba(self, capsys):
        """Testa email sem @"""
        resultado = validar_email("usuarioexample.com")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_email_sem_dominio(self, capsys):
        """Testa email sem domínio após @"""
        resultado = validar_email("usuario@")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_email_sem_extensao(self, capsys):
        """Testa email sem extensão (.com, .br, etc)"""
        resultado = validar_email("usuario@example")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_email_multiplos_arrobas(self, capsys):
        """Testa email com múltiplos @"""
        resultado = validar_email("usuario@@example.com")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_email_vazio(self, capsys):
        """Testa email vazio"""
        resultado = validar_email("")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_email_com_espacos(self, capsys):
        """Testa email com espaços"""
        resultado = validar_email("usuario @example.com")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out


class TestValidarTelefone:
    """Testes para validação de telefone brasileiro"""
    
    def test_telefone_11_digitos(self):
        """Testa telefone com 11 dígitos (celular)"""
        resultado = validar_telefone("11987654321")
        assert resultado == "(11) 98765-4321"
    
    def test_telefone_10_digitos(self):
        """Testa telefone com 10 dígitos (fixo)"""
        resultado = validar_telefone("1133334444")
        assert resultado == "(11) 3333-4444"
    
    def test_telefone_com_formatacao(self):
        """Testa telefone já formatado"""
        resultado = validar_telefone("(11) 98765-4321")
        assert resultado == "(11) 98765-4321"
    
    def test_telefone_com_espacos(self):
        """Testa telefone com espaços"""
        resultado = validar_telefone("11 9 8765 4321")
        assert resultado == "(11) 98765-4321"
    
    def test_telefone_invalido_poucos_digitos(self, capsys):
        """Testa telefone com poucos dígitos"""
        resultado = validar_telefone("12345")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_telefone_invalido_muitos_digitos(self, capsys):
        """Testa telefone com muitos dígitos"""
        resultado = validar_telefone("119876543210")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_telefone_invalido_letras(self, capsys):
        """Testa telefone contendo letras"""
        resultado = validar_telefone("11abc98765")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_telefone_vazio(self, capsys):
        """Testa telefone vazio"""
        resultado = validar_telefone("")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out


class TestValidarCPF:
    """Testes para validação de CPF"""
    
    def test_cpf_valido(self):
        """Testa CPF válido (exemplo do teste)"""
        resultado = validar_cpf("11144477735")
        assert resultado == "111.444.777-35"
    
    def test_cpf_com_formatacao(self):
        """Testa CPF já formatado"""
        resultado = validar_cpf("111.444.777-35")
        assert resultado == "111.444.777-35"
    
    def test_cpf_com_espacos(self):
        """Testa CPF com espaços"""
        resultado = validar_cpf("111 444 777 35")
        assert resultado == "111.444.777-35"
    
    def test_cpf_invalido_poucos_digitos(self, capsys):
        """Testa CPF com poucos dígitos"""
        resultado = validar_cpf("12345")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_cpf_invalido_muitos_digitos(self, capsys):
        """Testa CPF com muitos dígitos"""
        resultado = validar_cpf("123456789012")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_cpf_invalido_todos_iguais(self, capsys):
        """Testa CPF com todos os dígitos iguais"""
        resultado = validar_cpf("11111111111")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_cpf_invalido_digito_verificador(self, capsys):
        """Testa CPF com dígito verificador errado"""
        resultado = validar_cpf("11144477736")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_cpf_invalido_letras(self, capsys):
        """Testa CPF contendo letras"""
        resultado = validar_cpf("111abc77735")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_cpf_vazio(self, capsys):
        """Testa CPF vazio"""
        resultado = validar_cpf("")
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out


class TestValidarOpcao:
    """Testes para validação de opcões"""
    
    def test_opcao_valida(self):
        """Testa opção válida"""
        opcoes = ["a", "b", "c"]
        assert validar_opcao("a", opcoes) == "a"
        assert validar_opcao("b", opcoes) == "b"
    
    def test_opcao_invalida(self, capsys):
        """Testa opção inválida"""
        opcoes = ["a", "b", "c"]
        resultado = validar_opcao("d", opcoes)
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_opcao_vazia(self, capsys):
        """Testa opção vazia"""
        opcoes = ["a", "b", "c"]
        resultado = validar_opcao("", opcoes)
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_opcao_case_sensitive(self, capsys):
        """Testa que validação é sensível a maiúsculas/minúsculas"""
        opcoes = ["A", "B", "C"]
        resultado = validar_opcao("a", opcoes)
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    def test_opcao_numeros(self):
        """Testa opções numéricas"""
        opcoes = ["1", "2", "3"]
        assert validar_opcao("1", opcoes) == "1"
        resultado = validar_opcao("4", opcoes)
        assert resultado is None


class TestCenariosComplexos:
    """Testes de cenários complexos e combinados"""
    
    def test_divisao_por_zero_simulada(self):
        """Simula validação para divisão por zero"""
        divisor = validar_float("0")
        assert divisor == 0.0
    
    def test_entrada_invalida_varias_vezes(self, capsys):
        """Testa múltiplas entradas inválidas seguidas"""
        assert validar_inteiro("abc") is None
        assert validar_inteiro("xyz") is None
        assert validar_inteiro("!@#") is None
        captured = capsys.readouterr()
        assert captured.out.count("Erro") >= 3
    
    def test_validacao_encadeada(self):
        """Testa validação com múltiplas camadas"""
        numero = validar_inteiro("50", minimo=10, maximo=100)
        assert numero == 50
        
        if numero is not None:
            resultado = validar_opcao(str(numero), ["50", "60", "70"])
            assert resultado == "50"
    
    def test_sanitizacao_entrada(self):
        """Testa limpeza de espaços em entrada"""
        assert validar_inteiro("  42  ") == 42
        assert validar_texto("  Olá  ") == "Olá"
    
    @pytest.mark.parametrize("entrada_invalida", [
        "!@#$%",
        "None",
        "null",
        "undefined",
        "<script>",
        "'; DROP TABLE--",
    ])
    def test_entradas_maliciosas(self, entrada_invalida, capsys):
        """Testa entradas potencialmente maliciosas"""
        resultado = validar_inteiro(entrada_invalida)
        assert resultado is None
        captured = capsys.readouterr()
        assert "Erro" in captured.out
    
    @pytest.mark.parametrize("valor_invalido,minimo,maximo", [
        ("9", 10, 20),
        ("21", 10, 20),
        ("-1", 0, 100),
        ("101", 0, 100),
    ])
    def test_valores_fora_intervalo(self, valor_invalido, minimo, maximo):
        """Testa valores fora do intervalo permitido"""
        resultado = validar_inteiro(valor_invalido, minimo=minimo, maximo=maximo)
        assert resultado is None
    
    def test_tratamento_tipo_none(self):
        """Testa comportamento com None implícito"""
        resultado = validar_inteiro("not_a_number")
        assert resultado is None
    
    def test_consistencia_mensagens_erro(self, capsys):
        """Testa que mensagens de erro são consistentes"""
        validar_inteiro("abc")
        output1 = capsys.readouterr().out
        
        validar_inteiro("xyz")
        output2 = capsys.readouterr().out
        
        assert "Erro" in output1
        assert "Erro" in output2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-ra"])