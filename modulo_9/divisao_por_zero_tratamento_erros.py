class Calculadora:
    """Classe que realiza operações matemáticas com tratamento de erros."""
    
    def dividir(self, a, b):
        """
        Realiza divisão com tratamento de erro para divisão por zero.
        
        Args:
            a (float): Dividendo
            b (float): Divisor
        
        Returns:
            float: Resultado da divisão ou None se erro
        """
        try:
            if b == 0:
                raise ZeroDivisionError("Impossível dividir por zero!")
            resultado = a / b
            return resultado
        except ZeroDivisionError as erro:
            print(f"❌ ERRO: {erro}")
            return None
        except TypeError:
            print("❌ ERRO: Tipo de dado inválido! Use números.")
            return None
    
    def somar(self, a, b):
        """Soma dois números."""
        try:
            return a + b
        except TypeError:
            print("❌ ERRO: Tipo de dado inválido! Use números.")
            return None
    
    def subtrair(self, a, b):
        """Subtrai dois números."""
        try:
            return a - b
        except TypeError:
            print("❌ ERRO: Tipo de dado inválido! Use números.")
            return None
    
    def multiplicar(self, a, b):
        """Multiplica dois números."""
        try:
            return a * b
        except TypeError:
            print("❌ ERRO: Tipo de dado inválido! Use números.")
            return None


def calculadora_interativa():
    """Função que executa uma calculadora interativa com tratamento de erros."""
    calc = Calculadora()
    
    print("\n" + "=" * 60)
    print(" CALCULADORA COM TRATAMENTO DE ERROS")
    print("=" * 60)
    print("\nOperações disponíveis: +, -, *, /")
    print("Digite 'sair' para encerrar\n")
    
    while True:
        try:
            entrada = input("Digite a operação (ex: 10 + 5): ").strip()
            
            if entrada.lower() == "sair":
                print("Encerrando calculadora...")
                break
            
            # Separar entrada em partes
            partes = entrada.split()
            
            if len(partes) != 3:
                print("❌ ERRO: Formato inválido! Use: número operador número\n")
                continue
            
            try:
                num1 = float(partes[0])
                operacao = partes[1]
                num2 = float(partes[2])
            except ValueError:
                print("❌ ERRO: Os valores devem ser números!\n")
                continue
            
            # Executar operação
            if operacao == "+":
                resultado = calc.somar(num1, num2)
            elif operacao == "-":
                resultado = calc.subtrair(num1, num2)
            elif operacao == "*":
                resultado = calc.multiplicar(num1, num2)
            elif operacao == "/":
                resultado = calc.dividir(num1, num2)
            else:
                print(f"❌ ERRO: Operação '{operacao}' não reconhecida!\n")
                continue
            
            if resultado is not None:
                print(f"✓ Resultado: {num1} {operacao} {num2} = {resultado}\n")
            else:
                print()
        
        except KeyboardInterrupt:
            print("\n\nCalculadora interrompida pelo usuário.")
            break
        except Exception as erro:
            print(f"❌ ERRO inesperado: {erro}\n")


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" EXEMPLOS: DIVISÃO COM TRATAMENTO DE ERROS")
    print("=" * 60 + "\n")
    
    calc = Calculadora()
    
    # Exemplo 1: Divisão normal
    print("--- Exemplo 1: Divisão Normal ---")
    resultado = calc.dividir(10, 2)
    print(f"10 ÷ 2 = {resultado}\n")
    
    # Exemplo 2: Divisão por zero
    print("--- Exemplo 2: Divisão por Zero (Erro) ---")
    resultado = calc.dividir(10, 0)
    print(f"Resultado: {resultado}\n")
    
    # Exemplo 3: Divisão com resultado decimal
    print("--- Exemplo 3: Divisão com Resultado Decimal ---")
    resultado = calc.dividir(7, 2)
    print(f"7 ÷ 2 = {resultado}\n")
    
    # Exemplo 4: Tipo de dado inválido
    print("--- Exemplo 4: Tipo de Dado Inválido (Erro) ---")
    resultado = calc.dividir("10", 2)
    print(f"Resultado: {resultado}\n")
    
    # Exemplo 5: Outras operações
    print("--- Exemplo 5: Outras Operações ---")
    print(f"10 + 5 = {calc.somar(10, 5)}")
    print(f"10 - 3 = {calc.subtrair(10, 3)}")
    print(f"10 × 5 = {calc.multiplicar(10, 5)}\n")
    
    # Exemplo 6: Operações com erros
    print("--- Exemplo 6: Operações com Erros ---")
    print(f"10 + 'texto' = {calc.somar(10, 'texto')}")
    print()
    
    # Iniciar calculadora interativa
    print("\n" + "=" * 60)
    print(" CALCULADORA INTERATIVA")
    print("=" * 60)
    resposta = input("Deseja usar a calculadora interativa? (s/n): ").strip().lower()
    
    if resposta == "s":
        calculadora_interativa()