import re
from typing import Union


# ============================================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================================

def validar_inteiro(valor: str, minimo: int = None, maximo: int = None) -> Union[int, None]:
    """
    Valida se uma string é um número inteiro válido.
    
    Args:
        valor (str): String a validar
        minimo (int): Valor mínimo (opcional)
        maximo (int): Valor máximo (opcional)
    
    Returns:
        int: Número inteiro se válido, None caso contrário
    """
    try:
        numero = int(valor)
        
        if minimo is not None and numero < minimo:
            print(f"❌ Erro: Número deve ser maior ou igual a {minimo}")
            return None
        
        if maximo is not None and numero > maximo:
            print(f"❌ Erro: Número deve ser menor ou igual a {maximo}")
            return None
        
        return numero
    
    except ValueError:
        print(f"❌ Erro: '{valor}' não é um número inteiro válido")
        return None


def validar_float(valor: str, minimo: float = None, maximo: float = None) -> Union[float, None]:
    """
    Valida se uma string é um número decimal válido.
    
    Args:
        valor (str): String a validar
        minimo (float): Valor mínimo (opcional)
        maximo (float): Valor máximo (opcional)
    
    Returns:
        float: Número decimal se válido, None caso contrário
    """
    try:
        numero = float(valor)
        
        if minimo is not None and numero < minimo:
            print(f"❌ Erro: Número deve ser maior ou igual a {minimo}")
            return None
        
        if maximo is not None and numero > maximo:
            print(f"❌ Erro: Número deve ser menor ou igual a {maximo}")
            return None
        
        return numero
    
    except ValueError:
        print(f"❌ Erro: '{valor}' não é um número decimal válido")
        return None


def validar_idade(valor: str) -> Union[int, None]:
    """
    Valida se a entrada é uma idade válida.
    
    Args:
        valor (str): String a validar
    
    Returns:
        int: Idade se válida, None caso contrário
    """
    idade = validar_inteiro(valor, minimo=0, maximo=150)
    
    if idade is not None and idade < 18:
        print("⚠ Aviso: Menor de idade (< 18 anos)")
    
    return idade


def validar_texto(valor: str, minimo_caracteres: int = 1, 
                  maximo_caracteres: int = None) -> Union[str, None]:
    """
    Valida uma entrada de texto.
    
    Args:
        valor (str): String a validar
        minimo_caracteres (int): Mínimo de caracteres
        maximo_caracteres (int): Máximo de caracteres (opcional)
    
    Returns:
        str: Texto se válido, None caso contrário
    """
    valor = valor.strip()
    
    if len(valor) < minimo_caracteres:
        print(f"❌ Erro: Texto deve ter pelo menos {minimo_caracteres} caractere(s)")
        return None
    
    if maximo_caracteres is not None and len(valor) > maximo_caracteres:
        print(f"❌ Erro: Texto não pode exceder {maximo_caracteres} caracteres")
        return None
    
    return valor


def validar_email(valor: str) -> Union[str, None]:
    """
    Valida um endereço de email.
    
    Args:
        valor (str): Email a validar
    
    Returns:
        str: Email se válido, None caso contrário
    """
    # Padrão regex para email
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(padrao, valor):
        return valor
    else:
        print(f"❌ Erro: '{valor}' não é um email válido")
        return None


def validar_telefone(valor: str) -> Union[str, None]:
    """
    Valida um número de telefone brasileiro.
    
    Args:
        valor (str): Telefone a validar
    
    Returns:
        str: Telefone se válido, None caso contrário
    """
    # Remove caracteres não numéricos
    telefone = re.sub(r'\D', '', valor)
    
    if len(telefone) == 11:  # (XX) 9XXXX-XXXX
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:  # (XX) XXXX-XXXX
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    else:
        print(f"❌ Erro: Telefone deve ter 10 ou 11 dígitos")
        return None


def validar_cpf(valor: str) -> Union[str, None]:
    """
    Valida um CPF brasileiro.
    
    Args:
        valor (str): CPF a validar
    
    Returns:
        str: CPF se válido, None caso contrário
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', valor)
    
    if len(cpf) != 11:
        print(f"❌ Erro: CPF deve conter 11 dígitos")
        return None
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        print(f"❌ Erro: CPF inválido")
        return None
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        print(f"❌ Erro: CPF inválido")
        return None
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        print(f"❌ Erro: CPF inválido")
        return None
    
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validar_opcao(valor: str, opcoes: list) -> Union[str, None]:
    """
    Valida se o valor está em uma lista de opções.
    
    Args:
        valor (str): Valor a validar
        opcoes (list): Lista de opções válidas
    
    Returns:
        str: Valor se válido, None caso contrário
    """
    if valor in opcoes:
        return valor
    else:
        print(f"❌ Erro: Opção inválida. Opções válidas: {opcoes}")
        return None


# ============================================================================
# FUNÇÕES DE ENTRADA COM VALIDAÇÃO
# ============================================================================

def obter_inteiro(mensagem: str, minimo: int = None, maximo: int = None) -> int:
    """
    Obtém um número inteiro do usuário com validação repetida.
    
    Args:
        mensagem (str): Mensagem a exibir
        minimo (int): Valor mínimo
        maximo (int): Valor máximo
    
    Returns:
        int: Número inteiro validado
    """
    while True:
        try:
            entrada = input(mensagem)
            numero = validar_inteiro(entrada, minimo, maximo)
            if numero is not None:
                return numero
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            exit()
        except Exception as erro:
            print(f"❌ Erro: {erro}")


def obter_idade(mensagem: str = "Digite sua idade: ") -> int:
    """Obtém uma idade válida do usuário."""
    while True:
        try:
            entrada = input(mensagem)
            idade = validar_idade(entrada)
            if idade is not None:
                return idade
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            exit()
        except Exception as erro:
            print(f"❌ Erro: {erro}")


def obter_texto(mensagem: str, minimo: int = 1, maximo: int = None) -> str:
    """Obtém um texto válido do usuário."""
    while True:
        try:
            entrada = input(mensagem)
            texto = validar_texto(entrada, minimo, maximo)
            if texto is not None:
                return texto
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            exit()
        except Exception as erro:
            print(f"❌ Erro: {erro}")


def obter_email(mensagem: str = "Digite seu email: ") -> str:
    """Obtém um email válido do usuário."""
    while True:
        try:
            entrada = input(mensagem)
            email = validar_email(entrada)
            if email is not None:
                return email
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            exit()
        except Exception as erro:
            print(f"❌ Erro: {erro}")


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def formulario_cadastro():
    """Exemplo de formulário com validações completas."""
    print("\n" + "=" * 60)
    print(" FORMULÁRIO DE CADASTRO COM VALIDAÇÃO")
    print("=" * 60 + "\n")
    
    try:
        # Nome
        nome = obter_texto("Digite seu nome: ", minimo=3, maximo=100)
        
        # Idade
        idade = obter_idade("Digite sua idade: ")
        
        # Email
        email = obter_email("Digite seu email: ")
        
        # Telefone
        while True:
            telefone_entrada = input("Digite seu telefone: ")
            telefone = validar_telefone(telefone_entrada)
            if telefone is not None:
                break
        
        # CPF
        while True:
            cpf_entrada = input("Digite seu CPF: ")
            cpf = validar_cpf(cpf_entrada)
            if cpf is not None:
                break
        
        # Salário
        while True:
            salario_entrada = input("Digite seu salário: R$ ")
            salario = validar_float(salario_entrada, minimo=0)
            if salario is not None:
                break
        
        # Gênero
        while True:
            genero = input("Gênero (M/F/Outro): ").upper()
            if validar_opcao(genero, ["M", "F", "OUTRO"]):
                break
        
        # Exibir dados cadastrados
        print("\n" + "=" * 60)
        print(" DADOS CADASTRADOS")
        print("=" * 60)
        print(f"Nome: {nome}")
        print(f"Idade: {idade} anos")
        print(f"Email: {email}")
        print(f"Telefone: {telefone}")
        print(f"CPF: {cpf}")
        print(f"Salário: R$ {salario:.2f}")
        print(f"Gênero: {genero}")
        print("=" * 60 + "\n")
        
        print("✓ Cadastro realizado com sucesso!\n")
    
    except KeyboardInterrupt:
        print("\n\nCadastro cancelado pelo usuário.")


# ============================================================================
# EXEMPLOS DE VALIDAÇÃO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" EXEMPLOS DE VALIDAÇÃO DE ENTRADA")
    print("=" * 60 + "\n")
    
    # Teste 1: Validar idade
    print("--- Teste 1: Validar Idade ---")
    print("Testando: '25'")
    print(f"Resultado: {validar_idade('25')}\n")
    
    print("Testando: '-5'")
    print(f"Resultado: {validar_idade('-5')}\n")
    
    print("Testando: 'abc'")
    print(f"Resultado: {validar_idade('abc')}\n")
    
    # Teste 2: Validar email
    print("--- Teste 2: Validar Email ---")
    print("Testando: 'joao@email.com'")
    print(f"Resultado: {validar_email('joao@email.com')}\n")
    
    print("Testando: 'email_invalido'")
    print(f"Resultado: {validar_email('email_invalido')}\n")
    
    # Teste 3: Validar telefone
    print("--- Teste 3: Validar Telefone ---")
    print("Testando: '11987654321'")
    print(f"Resultado: {validar_telefone('11987654321')}\n")
    
    print("Testando: '123'")
    print(f"Resultado: {validar_telefone('123')}\n")
    
    # Teste 4: Validar CPF
    print("--- Teste 4: Validar CPF ---")
    print("Testando: '123.456.789-09' (inválido)")
    print(f"Resultado: {validar_cpf('123.456.789-09')}\n")
    
    # Iniciar formulário
    resposta = input("Deseja preencher o formulário de cadastro? (s/n): ").strip().lower()
    if resposta == "s":
        formulario_cadastro()