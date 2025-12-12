import sqlite3
import re
from datetime import datetime
from typing import List, Tuple, Optional, Dict


# ============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================================

BANCO_DADOS = "clientes_crud.db"


class GerenciadorClientes:
    """Classe para gerenciar operações CRUD na tabela Clientes."""
    
    def __init__(self, nome_banco: str = BANCO_DADOS):
        """Inicializa o gerenciador."""
        self.nome_banco = nome_banco
        self.conexao = None
    
    def conectar(self) -> bool:
        """Estabelece conexão com o banco de dados."""
        try:
            self.conexao = sqlite3.connect(self.nome_banco)
            self.conexao.row_factory = sqlite3.Row
            print(f"✓ Conectado ao banco: {self.nome_banco}\n")
            return True
        except sqlite3.Error as erro:
            print(f"❌ Erro de conexão: {erro}")
            return False
    
    def desconectar(self) -> None:
        """Fecha a conexão com o banco."""
        if self.conexao:
            self.conexao.close()
            print("✓ Conexão fechada\n")
    
    def criar_tabela(self) -> bool:
        """Cria a tabela Clientes."""
        try:
            cursor = self.conexao.cursor()
            sql = """
            CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(sql)
            self.conexao.commit()
            print("✓ Tabela 'Clientes' pronta\n")
            return True
        except sqlite3.Error as erro:
            print(f"❌ Erro ao criar tabela: {erro}")
            return False
    
    # ========================================================================
    # CREATE (CRIAR)
    # ========================================================================
    
    def validar_email(self, email: str) -> bool:
        """Valida formato do email."""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    def validar_telefone(self, telefone: str) -> bool:
        """Valida formato do telefone."""
        if not telefone:
            return True  # Telefone é opcional
        padrao = r'^\(\d{2}\)\s?\d{4,5}-\d{4}$|^\d{10,11}$'
        return re.match(padrao, telefone) is not None
    
    def inserir(self, nome: str, email: str, telefone: str = None) -> bool:
        """
        Insere um novo cliente.
        
        Args:
            nome: Nome do cliente
            email: Email do cliente
            telefone: Telefone (opcional)
        
        Returns:
            True se inserido com sucesso
        """
        # Validações
        if not nome or not email:
            print("❌ Nome e email são obrigatórios")
            return False
        
        if len(nome) < 3:
            print("❌ Nome deve ter pelo menos 3 caracteres")
            return False
        
        if not self.validar_email(email):
            print(f"❌ Email inválido: {email}")
            return False
        
        if telefone and not self.validar_telefone(telefone):
            print(f"❌ Telefone inválido: {telefone}")
            return False
        
        try:
            cursor = self.conexao.cursor()
            sql = "INSERT INTO Clientes (nome, email, telefone) VALUES (?, ?, ?)"
            cursor.execute(sql, (nome.strip(), email.strip(), telefone))
            self.conexao.commit()
            print(f"✓ Cliente '{nome}' inserido (ID: {cursor.lastrowid})")
            return True
        
        except sqlite3.IntegrityError:
            print(f"⚠️  Email já cadastrado: {email}")
            return False
        except sqlite3.Error as erro:
            print(f"❌ Erro ao inserir: {erro}")
            return False
    
    def inserir_multiplos(self, clientes: List[Tuple]) -> int:
        """
        Insere múltiplos clientes em uma transação.
        
        Args:
            clientes: Lista de tuplas (nome, email, telefone)
        
        Returns:
            Quantidade de clientes inseridos
        """
        inseridos = 0
        try:
            cursor = self.conexao.cursor()
            for nome, email, telefone in clientes:
                if self.validar_email(email):
                    try:
                        sql = "INSERT INTO Clientes (nome, email, telefone) VALUES (?, ?, ?)"
                        cursor.execute(sql, (nome, email, telefone))
                        inseridos += 1
                    except sqlite3.IntegrityError:
                        print(f"⚠️  Email duplicado ignorado: {email}")
            
            self.conexao.commit()
            return inseridos
        except sqlite3.Error as erro:
            print(f"❌ Erro ao inserir múltiplos: {erro}")
            self.conexao.rollback()
            return 0
    
    # ========================================================================
    # READ (LER/CONSULTAR)
    # ========================================================================
    
    def listar_todos(self) -> List:
        """Retorna todos os clientes."""
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Clientes ORDER BY id")
            return cursor.fetchall()
        except sqlite3.Error as erro:
            print(f"❌ Erro ao listar: {erro}")
            return []
    
    def buscar_por_id(self, cliente_id: int):
        """Busca cliente pelo ID."""
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Clientes WHERE id = ?", (cliente_id,))
            return cursor.fetchone()
        except sqlite3.Error as erro:
            print(f"❌ Erro ao buscar: {erro}")
            return None
    
    def buscar_por_email(self, email: str):
        """Busca cliente pelo email."""
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM Clientes WHERE email = ?", (email,))
            return cursor.fetchone()
        except sqlite3.Error as erro:
            print(f"❌ Erro ao buscar: {erro}")
            return None
    
    def buscar_por_nome(self, nome: str) -> List:
        """Busca clientes por nome (parcial)."""
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT * FROM Clientes WHERE nome LIKE ? ORDER BY nome",
                (f"%{nome}%",)
            )
            return cursor.fetchall()
        except sqlite3.Error as erro:
            print(f"❌ Erro ao buscar: {erro}")
            return []
    
    def buscar_com_filtro(self, **filtros) -> List:
        """
        Busca clientes com múltiplos filtros.
        
        Exemplo: buscar_com_filtro(nome="Ana", email="@gmail.com")
        """
        try:
            sql = "SELECT * FROM Clientes WHERE 1=1"
            parametros = []
            
            if "nome" in filtros:
                sql += " AND nome LIKE ?"
                parametros.append(f"%{filtros['nome']}%")
            
            if "email" in filtros:
                sql += " AND email LIKE ?"
                parametros.append(f"%{filtros['email']}%")
            
            if "telefone" in filtros:
                sql += " AND telefone LIKE ?"
                parametros.append(f"%{filtros['telefone']}%")
            
            sql += " ORDER BY nome"
            
            cursor = self.conexao.cursor()
            cursor.execute(sql, parametros)
            return cursor.fetchall()
        
        except sqlite3.Error as erro:
            print(f"❌ Erro ao buscar: {erro}")
            return []
    
    def contar_clientes(self) -> int:
        """Retorna o número total de clientes."""
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM Clientes")
            return cursor.fetchone()[0]
        except sqlite3.Error:
            return 0
    
    # ========================================================================
    # UPDATE (ATUALIZAR)
    # ========================================================================
    
    def atualizar(self, cliente_id: int, **dados) -> bool:
        """
        Atualiza dados de um cliente.
        
        Exemplo: atualizar(1, nome="Novo Nome", telefone="(11)99999-9999")
        """
        if not self.buscar_por_id(cliente_id):
            print(f"❌ Cliente ID {cliente_id} não encontrado")
            return False
        
        # Validar dados a atualizar
        if "email" in dados and not self.validar_email(dados["email"]):
            print(f"❌ Email inválido: {dados['email']}")
            return False
        
        if "telefone" in dados and dados["telefone"]:
            if not self.validar_telefone(dados["telefone"]):
                print(f"❌ Telefone inválido: {dados['telefone']}")
                return False
        
        try:
            campos = []
            valores = []
            
            for chave, valor in dados.items():
                if chave in ["nome", "email", "telefone"]:
                    campos.append(f"{chave} = ?")
                    valores.append(valor)
            
            if not campos:
                print("⚠️  Nenhum campo para atualizar")
                return False
            
            # Adicionar data de atualização
            campos.append("data_atualizacao = CURRENT_TIMESTAMP")
            valores.append(cliente_id)
            
            sql = f"UPDATE Clientes SET {', '.join(campos)} WHERE id = ?"
            
            cursor = self.conexao.cursor()
            cursor.execute(sql, valores)
            self.conexao.commit()
            
            print(f"✓ Cliente ID {cliente_id} atualizado com sucesso")
            return True
        
        except sqlite3.IntegrityError:
            print("⚠️  Email já cadastrado por outro cliente")
            return False
        except sqlite3.Error as erro:
            print(f"❌ Erro ao atualizar: {erro}")
            return False
    
    # ========================================================================
    # DELETE (DELETAR)
    # ========================================================================
    
    def deletar(self, cliente_id: int) -> bool:
        """Deleta um cliente."""
        cliente = self.buscar_por_id(cliente_id)
        
        if not cliente:
            print(f"❌ Cliente ID {cliente_id} não encontrado")
            return False
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM Clientes WHERE id = ?", (cliente_id,))
            self.conexao.commit()
            print(f"✓ Cliente '{cliente['nome']}' deletado com sucesso")
            return True
        
        except sqlite3.Error as erro:
            print(f"❌ Erro ao deletar: {erro}")
            return False
    
    def deletar_por_email(self, email: str) -> bool:
        """Deleta um cliente pelo email."""
        cliente = self.buscar_por_email(email)
        
        if not cliente:
            print(f"❌ Cliente com email '{email}' não encontrado")
            return False
        
        return self.deletar(cliente['id'])
    
    def limpar_tudo(self) -> bool:
        """Deleta TODOS os clientes (cuidado!)."""
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM Clientes")
            self.conexao.commit()
            print("✓ Todos os clientes foram deletados")
            return True
        except sqlite3.Error as erro:
            print(f"❌ Erro: {erro}")
            return False
    
    # ========================================================================
    # UTILITÁRIOS
    # ========================================================================
    
    def exportar_para_lista(self) -> List[Dict]:
        """Exporta clientes como lista de dicionários."""
        clientes = self.listar_todos()
        return [dict(cliente) for cliente in clientes]
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas sobre os clientes."""
        try:
            cursor = self.conexao.cursor()
            
            total = self.contar_clientes()
            
            cursor.execute("SELECT COUNT(*) FROM Clientes WHERE telefone IS NOT NULL")
            com_telefone = cursor.fetchone()[0]
            
            cursor.execute("SELECT MIN(data_cadastro) FROM Clientes")
            primeiro = cursor.fetchone()[0]
            
            cursor.execute("SELECT MAX(data_cadastro) FROM Clientes")
            ultimo = cursor.fetchone()[0]
            
            return {
                "total": total,
                "com_telefone": com_telefone,
                "sem_telefone": total - com_telefone,
                "primeiro_cadastro": primeiro,
                "ultimo_cadastro": ultimo
            }
        except sqlite3.Error:
            return {}


# ============================================================================
# FUNÇÕES DE EXIBIÇÃO
# ============================================================================

def exibir_tabela(clientes: List, titulo: str = "CLIENTES") -> None:
    """Exibe clientes em formato de tabela."""
    if not clientes:
        print("📭 Nenhum cliente encontrado\n")
        return
    
    print("\n" + "=" * 110)
    print(f"  {titulo}")
    print("=" * 110)
    print(f"{'ID':<5} {'Nome':<25} {'Email':<35} {'Telefone':<15} {'Cadastro':<15}")
    print("=" * 110)
    
    for cliente in clientes:
        id_c = cliente[0]
        nome = cliente[1][:22] + "..." if len(cliente[1]) > 25 else cliente[1]
        email = cliente[2][:32] + "..." if len(cliente[2]) > 35 else cliente[2]
        telefone = cliente[3] if cliente[3] else "N/A"
        data = cliente[4][:10]
        
        print(f"{id_c:<5} {nome:<25} {email:<35} {telefone:<15} {data:<15}")
    
    print("=" * 110 + "\n")


def exibir_cliente_completo(cliente) -> None:
    """Exibe detalhes completos de um cliente."""
    if not cliente:
        print("❌ Cliente não encontrado\n")
        return
    
    print("\n" + "=" * 60)
    print(f"  DETALHES DO CLIENTE")
    print("=" * 60)
    print(f"\n  ID:                {cliente[0]}")
    print(f"  Nome:              {cliente[1]}")
    print(f"  Email:             {cliente[2]}")
    print(f"  Telefone:          {cliente[3] if cliente[3] else 'N/A'}")
    print(f"  Data Cadastro:     {cliente[4]}")
    print(f"  Data Atualização:  {cliente[5]}")
    print("\n" + "=" * 60 + "\n")


# ============================================================================
# EXEMPLOS E TESTES
# ============================================================================

def exemplo_crud_completo():
    """Demonstra todas as operações CRUD."""
    
    gerenciador = GerenciadorClientes()
    
    if not gerenciador.conectar():
        return
    
    gerenciador.criar_tabela()
    
    print("=" * 70)
    print(" OPERAÇÕES CRUD - EXEMPLOS PRÁTICOS")
    print("=" * 70 + "\n")
    
    # ====== CREATE (Inserir) ======
    print("--- 1. CREATE: Inserindo Clientes ---\n")
    
    clientes_novos = [
        ("Maria Silva", "maria.silva@email.com", "(11) 98765-4321"),
        ("João Santos", "joao.santos@email.com", "(21) 99876-5432"),
        ("Ana Oliveira", "ana.oliveira@email.com", "(31) 97654-3210"),
        ("Carlos Costa", "carlos.costa@email.com", "(41) 98765-0123"),
        ("Fernanda Souza", "fernanda.souza@email.com", "(51) 99876-1234"),
    ]
    
    inseridos = gerenciador.inserir_multiplos(clientes_novos)
    print(f"\n✓ {inseridos} clientes inseridos\n")
    
    # ====== READ (Consultar) ======
    print("--- 2. READ: Consultando Todos os Clientes ---")
    todos = gerenciador.listar_todos()
    exibir_tabela(todos)
    
    # ====== READ por ID ======
    print("--- 3. READ: Buscando Cliente por ID ---\n")
    cliente = gerenciador.buscar_por_id(1)
    exibir_cliente_completo(cliente)
    
    # ====== READ por Email ======
    print("--- 4. READ: Buscando por Email ---\n")
    cliente = gerenciador.buscar_por_email("maria.silva@email.com")
    exibir_cliente_completo(cliente)
    
    # ====== READ por Nome (parcial) ======
    print("--- 5. READ: Buscando por Padrão de Nome ---")
    encontrados = gerenciador.buscar_por_nome("Silva")
    exibir_tabela(encontrados, "CLIENTES COM 'SILVA' NO NOME")
    
    # ====== READ com Filtros ======
    print("--- 6. READ: Buscando com Filtros ---")
    encontrados = gerenciador.buscar_com_filtro(email="@email.com")
    exibir_tabela(encontrados, f"CLIENTES COM EMAIL @email.com ({len(encontrados)})")
    
    # ====== UPDATE (Atualizar) ======
    print("--- 7. UPDATE: Atualizando Cliente ---\n")
    gerenciador.atualizar(2, telefone="(21) 98888-8888", nome="João Pedro Santos")
    cliente = gerenciador.buscar_por_id(2)
    exibir_cliente_completo(cliente)
    
    # ====== Validações ======
    print("--- 8. VALIDAÇÕES: Testando Dados Inválidos ---\n")
    
    print("Teste 1: Email inválido")
    gerenciador.inserir("Teste", "email_invalido", None)
    
    print("\nTeste 2: Email duplicado")
    gerenciador.inserir("Novo Cliente", "maria.silva@email.com", None)
    
    print("\nTeste 3: Nome muito curto")
    gerenciador.inserir("AB", "novo@email.com", None)
    
    print("\nTeste 4: Telefone inválido")
    gerenciador.inserir("Teste Válido", "teste@email.com", "123")
    print()
    
    # ====== Estatísticas ======
    print("--- 9. ESTATÍSTICAS ---\n")
    stats = gerenciador.obter_estatisticas()
    print(f"📊 Total de clientes:        {stats['total']}")
    print(f"☎️  Com telefone:             {stats['com_telefone']}")
    print(f"☎️  Sem telefone:             {stats['sem_telefone']}")
    print(f"📅 Primeiro cadastro:        {stats['primeiro_cadastro']}")
    print(f"📅 Último cadastro:          {stats['ultimo_cadastro']}\n")
    
    # ====== DELETE (Deletar) ======
    print("--- 10. DELETE: Deletando Cliente ---\n")
    gerenciador.deletar(5)
    print()
    
    # ====== Listagem Final ======
    print("--- 11. Listagem Final ---")
    todos = gerenciador.listar_todos()
    exibir_tabela(todos, f"CLIENTES FINAIS ({gerenciador.contar_clientes()})")
    
    # ====== Exportar ======
    print("--- 12. EXPORTAÇÃO: Convertendo para Lista de Dicionários ---\n")
    dados = gerenciador.exportar_para_lista()
    for cliente_dict in dados[:2]:
        print(f"  {cliente_dict}")
    print(f"  ... ({len(dados)} clientes no total)\n")
    
    gerenciador.desconectar()


def menu_interativo():
    """Menu interativo para gerenciar clientes."""
    
    gerenciador = GerenciadorClientes()
    
    if not gerenciador.conectar():
        return
    
    gerenciador.criar_tabela()
    
    while True:
        print("\n" + "=" * 50)
        print(" SISTEMA DE GERENCIAMENTO - OPERAÇÕES CRUD")
        print("=" * 50)
        print("\n[CREATE]  1. Inserir cliente")
        print("          2. Inserir múltiplos clientes")
        print("[READ]    3. Listar todos os clientes")
        print("          4. Buscar por ID")
        print("          5. Buscar por email")
        print("          6. Buscar por nome")
        print("[UPDATE]  7. Atualizar cliente")
        print("[DELETE]  8. Deletar cliente")
        print("[UTILS]   9. Ver estatísticas")
        print("          10. Ver exemplos")
        print("          0. Sair\n")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print()
            nome = input("Nome: ").strip()
            email = input("Email: ").strip()
            telefone = input("Telefone (opcional): ").strip() or None
            gerenciador.inserir(nome, email, telefone)
            print()
        
        elif opcao == "2":
            print("\n(Digite 'sair' para terminar)")
            clientes = []
            while True:
                nome = input("Nome: ").strip()
                if nome.lower() == "sair":
                    break
                email = input("Email: ").strip()
                telefone = input("Telefone: ").strip() or None
                clientes.append((nome, email, telefone))
            
            if clientes:
                inseridos = gerenciador.inserir_multiplos(clientes)
                print(f"\n✓ {inseridos} clientes inseridos\n")
        
        elif opcao == "3":
            todos = gerenciador.listar_todos()
            exibir_tabela(todos)
        
        elif opcao == "4":
            try:
                cliente_id = int(input("\nID do cliente: "))
                cliente = gerenciador.buscar_por_id(cliente_id)
                exibir_cliente_completo(cliente)
            except ValueError:
                print("❌ ID deve ser um número\n")
        
        elif opcao == "5":
            email = input("\nEmail: ").strip()
            cliente = gerenciador.buscar_por_email(email)
            exibir_cliente_completo(cliente)
        
        elif opcao == "6":
            nome = input("\nNome (parcial): ").strip()
            encontrados = gerenciador.buscar_por_nome(nome)
            exibir_tabela(encontrados, f"RESULTADO DA BUSCA")
        
        elif opcao == "7":
            try:
                cliente_id = int(input("\nID do cliente: "))
                print("(Deixe em branco para não alterar)")
                nome = input("Novo nome: ").strip() or None
                email = input("Novo email: ").strip() or None
                telefone = input("Novo telefone: ").strip() or None
                gerenciador.atualizar(cliente_id, nome=nome, email=email, telefone=telefone)
                print()
            except ValueError:
                print("❌ ID deve ser um número\n")
        
        elif opcao == "8":
            try:
                cliente_id = int(input("\nID do cliente: "))
                confirmacao = input("Tem certeza? (s/n): ").lower().strip()
                if confirmacao == "s":
                    gerenciador.deletar(cliente_id)
                print()
            except ValueError:
                print("❌ ID deve ser um número\n")
        
        elif opcao == "9":
            stats = gerenciador.obter_estatisticas()
            print(f"\n📊 Total: {stats['total']}")
            print(f"☎️  Com telefone: {stats['com_telefone']}")
            print(f"☎️  Sem telefone: {stats['sem_telefone']}\n")
        
        elif opcao == "10":
            gerenciador.desconectar()
            exemplo_crud_completo()
            gerenciador.conectar()
            gerenciador.criar_tabela()
        
        elif opcao == "0":
            print("\n👋 Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida\n")
    
    gerenciador.desconectar()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    # Executar exemplos automaticamente
    exemplo_crud_completo()
    
    # Descomente abaixo para usar o menu interativo
    # menu_interativo()