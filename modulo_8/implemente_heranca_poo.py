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


class CarroEletrico(Carro):
    """Classe que representa um carro elétrico, herdando de Carro."""
    
    def __init__(self, marca, modelo, autonomia_bateria):
        """
        Inicializa um objeto CarroEletrico com marca, modelo e autonomia da bateria.
        
        Args:
            marca (str): A marca do carro
            modelo (str): O modelo do carro
            autonomia_bateria (float): A autonomia da bateria em km
        """
        super().__init__(marca, modelo)
        self.autonomia_bateria = autonomia_bateria
    
    def exibir_info(self):
        """Exibe as informações do carro elétrico, incluindo autonomia da bateria."""
        super().exibir_info()
        print(f"Autonomia da bateria: {self.autonomia_bateria} km")


# Exemplo de uso
if __name__ == "__main__":
    # Criando um carro comum
    carro_comum = Carro("Honda", "Civic")
    print("--- Carro Comum ---")
    carro_comum.exibir_info()
    
    print("\n--- Carros Elétricos ---")
    # Criando carros elétricos
    carro_eletrico1 = CarroEletrico("Tesla", "Model 3", 560)
    carro_eletrico2 = CarroEletrico("Nissan", "Leaf", 415)
    
    carro_eletrico1.exibir_info()
    print()
    carro_eletrico2.exibir_info()