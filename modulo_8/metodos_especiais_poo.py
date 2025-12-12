class Carro:
    """Classe que demonstra o uso de métodos especiais __init__ e __str__."""
    
    def __init__(self, marca, modelo, ano):
        """
        Método especial __init__: inicializa os atributos do objeto.
        É chamado automaticamente quando um objeto é criado.
        
        Args:
            marca (str): A marca do carro
            modelo (str): O modelo do carro
            ano (int): O ano de fabricação
        """
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
    
    def __str__(self):
        """
        Método especial __str__: define como o objeto será exibido
        quando convertido para string (print, str()).
        
        Returns:
            str: Uma representação legível do objeto
        """
        return f"{self.ano} {self.marca} {self.modelo}"
    
    def __repr__(self):
        """
        Método especial __repr__: define uma representação técnica do objeto
        (útil para debugging).
        
        Returns:
            str: Uma representação técnica do objeto
        """
        return f"Carro(marca='{self.marca}', modelo='{self.modelo}', ano={self.ano})"


class Pessoa:
    """Outra classe para demonstrar os métodos especiais."""
    
    def __init__(self, nome, idade, profissao):
        """Inicializa os atributos da pessoa."""
        self.nome = nome
        self.idade = idade
        self.profissao = profissao
    
    def __str__(self):
        """Exibição amigável da pessoa."""
        return f"{self.nome}, {self.idade} anos, {self.profissao}"
    
    def __repr__(self):
        """Representação técnica da pessoa."""
        return f"Pessoa(nome='{self.nome}', idade={self.idade}, profissao='{self.profissao}')"


# Exemplo de uso
if __name__ == "__main__":
    print("=" * 60)
    print("DEMONSTRAÇÃO DE MÉTODOS ESPECIAIS: __init__ e __str__")
    print("=" * 60)
    
    # Criando objetos Carro
    # O método __init__ é chamado automaticamente
    carro1 = Carro("Toyota", "Corolla", 2020)
    carro2 = Carro("Ford", "Mustang", 2022)
    carro3 = Carro("Volkswagen", "Gol", 2019)
    
    print("\n--- CLASSE CARRO ---")
    print("\nUsando print() (chama __str__):")
    print(carro1)
    print(carro2)
    print(carro3)
    
    print("\nUsando repr() (chama __repr__):")
    print(repr(carro1))
    print(repr(carro2))
    
    print("\nAcessando atributos diretamente:")
    print(f"Marca: {carro1.marca}")
    print(f"Modelo: {carro1.modelo}")
    print(f"Ano: {carro1.ano}")
    
    # Criando objetos Pessoa
    print("\n" + "=" * 60)
    print("--- CLASSE PESSOA ---")
    print("=" * 60)
    
    pessoa1 = Pessoa("Ana Silva", 28, "Engenheira")
    pessoa2 = Pessoa("Carlos Santos", 35, "Professor")
    pessoa3 = Pessoa("Maria Oliveira", 42, "Médica")
    
    print("\nUsando print() (chama __str__):")
    print(pessoa1)
    print(pessoa2)
    print(pessoa3)
    
    print("\nUsando repr() (chama __repr__):")
    print(repr(pessoa1))
    
    print("\nCriando uma lista de pessoas:")
    pessoas = [pessoa1, pessoa2, pessoa3]
    for pessoa in pessoas:
        print(f"  - {pessoa}")
    
    print("\n" + "=" * 60)
    print("RESUMO DOS MÉTODOS ESPECIAIS:")
    print("=" * 60)
    print("""
__init__(self, ...):
  - Método construtor que inicializa os atributos do objeto
  - É chamado automaticamente quando o objeto é criado
  - É obrigatório que exista em qualquer classe

__str__(self):
  - Define como o objeto será exibido como string
  - Usado por print() e str()
  - Deve retornar uma string legível e amigável ao usuário
  
__repr__(self):
  - Define uma representação técnica do objeto
  - Usada por repr() e no console interativo
  - Útil para debugging e desenvolvimento
  - Idealmente deve parecer um comando Python válido
    """)