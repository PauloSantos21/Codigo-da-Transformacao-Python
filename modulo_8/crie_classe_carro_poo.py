class Carro:
    """Classe que representa um carro com seus atributos básicos."""
    
    def __init__(self, marca, modelo):
        """
        Inicializa um objeto Carro com marca e modelo.
        
        Args:
            marca (str): A marca do carro
            modelo (str): O modelo do carro
        """
        self.marca = marca
        self.modelo = modelo
    
    def exibir_info(self):
        """Exibe as informações do carro."""
        print(f"Carro: {self.marca} {self.modelo}")


# Exemplo de uso
if __name__ == "__main__":
    # Criando objetos da classe Carro
    carro1 = Carro("Toyota", "Corolla")
    carro2 = Carro("Ford", "Mustang")
    carro3 = Carro("Volkswagen", "Gol")
    
    # Exibindo informações dos carros
    carro1.exibir_info()
    carro2.exibir_info()
    carro3.exibir_info()