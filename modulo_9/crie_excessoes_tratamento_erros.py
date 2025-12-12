from datetime import datetime


# ============================================================================
# EXCEÇÕES PERSONALIZADAS
# ============================================================================

class SaldoInsuficienteError(Exception):
    """Exceção levantada quando há tentativa de saque com saldo insuficiente."""
    
    def __init__(self, saldo_atual, valor_solicitado):
        """
        Inicializa a exceção com informações detalhadas.
        
        Args:
            saldo_atual (float): Saldo atual da conta
            valor_solicitado (float): Valor solicitado para saque
        """
        self.saldo_atual = saldo_atual
        self.valor_solicitado = valor_solicitado
        self.diferenca = valor_solicitado - saldo_atual
        
        mensagem = (
            f"Saldo insuficiente! Saldo disponível: R$ {saldo_atual:.2f}, "
            f"valor solicitado: R$ {valor_solicitado:.2f}. "
            f"Faltam: R$ {self.diferenca:.2f}"
        )
        super().__init__(mensagem)


class LimiteExcedidoError(Exception):
    """Exceção levantada quando operação ultrapassa limite de transações."""
    
    def __init__(self, limite, operacoes_realizadas):
        mensagem = (
            f"Limite de operações diárias excedido! "
            f"Limite: {limite}, Realizadas: {operacoes_realizadas}"
        )
        super().__init__(mensagem)


class DepositoNegativoError(Exception):
    """Exceção levantada para depósitos com valores negativos."""
    
    def __init__(self, valor):
        mensagem = f"Valor de depósito não pode ser negativo! Valor recebido: R$ {valor:.2f}"
        super().__init__(mensagem)


# ============================================================================
# CLASSE CONTA BANCÁRIA
# ============================================================================

class ContaBancaria:
    """Classe que simula uma conta bancária com operações básicas."""
    
    def __init__(self, titular, numero_conta, saldo_inicial=0.0):
        """
        Inicializa uma conta bancária.
        
        Args:
            titular (str): Nome do titular
            numero_conta (str): Número da conta
            saldo_inicial (float): Saldo inicial (padrão: 0.0)
        """
        self.titular = titular
        self.numero_conta = numero_conta
        self._saldo = saldo_inicial
        self.historico = []
        self.limite_diario = 5000.0
        self.operacoes_hoje = 0
        self._registrar_operacao("ABERTURA", saldo_inicial, saldo_inicial)
    
    def _registrar_operacao(self, tipo, valor, saldo_resultante):
        """Registra uma operação no histórico."""
        operacao = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": tipo,
            "valor": valor,
            "saldo": saldo_resultante
        }
        self.historico.append(operacao)
    
    @property
    def saldo(self):
        """Retorna o saldo atual."""
        return self._saldo
    
    def depositar(self, valor):
        """
        Realiza um depósito na conta.
        
        Args:
            valor (float): Valor a depositar
        
        Raises:
            DepositoNegativoError: Se valor for negativo
        
        Returns:
            bool: True se sucesso
        """
        try:
            if valor < 0:
                raise DepositoNegativoError(valor)
            
            if valor == 0:
                print("⚠ Aviso: Não é possível depositar valor zero.\n")
                return False
            
            self._saldo += valor
            self._registrar_operacao("DEPÓSITO", valor, self._saldo)
            print(f"✓ Depósito de R$ {valor:.2f} realizado com sucesso!")
            print(f"  Novo saldo: R$ {self._saldo:.2f}\n")
            return True
        
        except DepositoNegativoError as erro:
            print(f"❌ ERRO: {erro}\n")
            return False
        except Exception as erro:
            print(f"❌ ERRO inesperado: {erro}\n")
            return False
    
    def sacar(self, valor):
        """
        Realiza um saque na conta.
        
        Args:
            valor (float): Valor a sacar
        
        Raises:
            SaldoInsuficienteError: Se saldo for insuficiente
            LimiteExcedidoError: Se exceder limite diário
        
        Returns:
            bool: True se sucesso
        """
        try:
            if valor < 0:
                print("❌ ERRO: Valor de saque não pode ser negativo!\n")
                return False
            
            if valor == 0:
                print("⚠ Aviso: Não é possível sacar valor zero.\n")
                return False
            
            if self.operacoes_hoje >= 3:
                raise LimiteExcedidoError(3, self.operacoes_hoje)
            
            if valor > self._saldo:
                raise SaldoInsuficienteError(self._saldo, valor)
            
            if valor > self.limite_diario:
                print(f"❌ ERRO: Valor ({valor}) ultrapassa limite diário de R$ {self.limite_diario:.2f}\n")
                return False
            
            self._saldo -= valor
            self.operacoes_hoje += 1
            self._registrar_operacao("SAQUE", valor, self._saldo)
            print(f"✓ Saque de R$ {valor:.2f} realizado com sucesso!")
            print(f"  Novo saldo: R$ {self._saldo:.2f}\n")
            return True
        
        except SaldoInsuficienteError as erro:
            print(f"❌ ERRO: {erro}\n")
            return False
        except LimiteExcedidoError as erro:
            print(f"❌ ERRO: {erro}\n")
            return False
        except Exception as erro:
            print(f"❌ ERRO inesperado: {erro}\n")
            return False
    
    def transferir(self, conta_destino, valor):
        """
        Realiza transferência para outra conta.
        
        Args:
            conta_destino (ContaBancaria): Conta destino
            valor (float): Valor a transferir
        
        Returns:
            bool: True se sucesso
        """
        try:
            print(f"Transferindo R$ {valor:.2f} para {conta_destino.titular}...")
            
            if not self.sacar(valor):
                return False
            
            if not conta_destino.depositar(valor):
                # Se depositou em erro, devolver valor
                self._saldo += valor
                return False
            
            self._registrar_operacao(
                f"TRANSFERÊNCIA ENVIADA",
                valor,
                self._saldo
            )
            conta_destino._registrar_operacao(
                f"TRANSFERÊNCIA RECEBIDA",
                valor,
                conta_destino._saldo
            )
            
            print(f"✓ Transferência realizada com sucesso!\n")
            return True
        
        except Exception as erro:
            print(f"❌ ERRO na transferência: {erro}\n")
            return False
    
    def exibir_saldo(self):
        """Exibe o saldo atual."""
        print(f"\n{'='*60}")
        print(f"Conta: {self.numero_conta}")
        print(f"Titular: {self.titular}")
        print(f"Saldo: R$ {self._saldo:.2f}")
        print(f"{'='*60}\n")
    
    def exibir_historico(self):
        """Exibe o histórico de operações."""
        print(f"\n{'='*60}")
        print(f"HISTÓRICO - Conta {self.numero_conta}")
        print(f"{'='*60}")
        
        for operacao in self.historico:
            print(f"[{operacao['data']}] {operacao['tipo']}: "
                  f"R$ {operacao['valor']:>10.2f} | "
                  f"Saldo: R$ {operacao['saldo']:>10.2f}")
        
        print(f"{'='*60}\n")


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SISTEMA BANCÁRIO COM EXCEÇÕES PERSONALIZADAS")
    print("=" * 60 + "\n")
    
    # Criar contas
    conta1 = ContaBancaria("João Silva", "001-5", 1000.0)
    conta2 = ContaBancaria("Maria Santos", "002-5", 500.0)
    
    # Exemplo 1: Depósito bem-sucedido
    print("--- Exemplo 1: Depósito Bem-sucedido ---")
    conta1.depositar(500.0)
    
    # Exemplo 2: Saque bem-sucedido
    print("--- Exemplo 2: Saque Bem-sucedido ---")
    conta1.sacar(200.0)
    
    # Exemplo 3: Saque com saldo insuficiente (ERRO)
    print("--- Exemplo 3: Saque com Saldo Insuficiente (Exceção) ---")
    conta1.sacar(2000.0)
    
    # Exemplo 4: Depósito negativo (ERRO)
    print("--- Exemplo 4: Depósito Negativo (Exceção) ---")
    conta1.depositar(-500.0)
    
    # Exemplo 5: Transferência bem-sucedida
    print("--- Exemplo 5: Transferência Bem-sucedida ---")
    conta1.transferir(conta2, 300.0)
    
    # Exemplo 6: Transferência com saldo insuficiente (ERRO)
    print("--- Exemplo 6: Transferência com Saldo Insuficiente (Exceção) ---")
    conta2.transferir(conta1, 5000.0)
    
    # Exemplo 7: Múltiplos saques
    print("--- Exemplo 7: Múltiplos Saques ---")
    conta1.sacar(100.0)
    conta1.sacar(100.0)
    conta1.sacar(100.0)
    conta1.sacar(100.0)  # Tentará ultrapassar limite
    
    # Exibir saldos finais
    print("--- Saldos Finais ---")
    conta1.exibir_saldo()
    conta2.exibir_saldo()
    
    # Exibir históricos
    conta1.exibir_historico()
    conta2.exibir_historico()