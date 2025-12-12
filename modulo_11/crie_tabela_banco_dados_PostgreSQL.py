import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


# ============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS SQLite
# ============================================================================

# Nome do arquivo do banco de dados
BANCO_DADOS = "clientes.db"

def conectar_banco():
    """Estabelece conexão com o banco de dados SQLite."""
    try:
        conexao = sqlite3.connect(BANCO_DADOS)
        conexao.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        print(f"✓ Conectado ao banco de dados: {BANCO_DADOS}\n")
        return conexao
    except sqlite3.Error as erro:
        print(f"❌ Erro ao conectar ao banco: {erro}")
        return None


def criar_tabela_clientes(conexao):
    """Cria a tabela Clientes se ela não existir."""
    try:
        cursor = conexao.cursor()
        
        # SQL para criar a tabela Clientes
        sql_criar_tabela = """
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(sql_criar_tabela)
        conexao.commit()
        print("✓ Tabela 'Clientes' criada com sucesso (ou já existe)\n")
        
    except sqlite3.Error as erro:
        print(f"❌ Erro ao criar tabela: {erro}")


# ============================================================================
# OPERAÇÕES BÁSICAS (CRUD: Create, Read, Update, Delete)
# ============================================================================

def inserir_cliente(conexao, nome: str, email: str, telefone: str = None) -> bool:
    """
    Insere um novo cliente na tabela.
    
    Args:
        conexao: Conexão com o banco
        nome: Nome do cliente
        email: Email do cliente
        telefone: Telefone do cliente (opcional)
    
    Returns:
        True se inserido com sucesso, False caso contrário
    """
    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO Clientes (nome, email, telefone) VALUES (?, ?, ?)"
        cursor.execute(sql, (nome, email, telefone))
        conexao.commit()
        print(f"✓ Cliente '{nome}' inserido com sucesso (ID: {cursor.lastrowid})")
        return True
    except sqlite3.IntegrityError as erro:
        print(f"⚠️  Email já cadastrado: {email}")
        return False
    except sqlite3.Error as erro:
        print(f"❌ Erro ao inserir cliente: {erro}")
        return False


def listar_clientes(conexao) -> List[Tuple]:
    """
    Lista todos os clientes cadastrados.
    
    Args:
        conexao: Conexão com o banco
    
    Returns:
        Lista de tuplas com dados dos clientes
    """
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Clientes ORDER BY id")
        clientes = cursor.fetchall()
        return clientes
    except sqlite3.Error as erro:
        print(f"❌ Erro ao listar clientes: {erro}")
        return []


def buscar_cliente_por_id(conexao, cliente_id: int):
    """
    Busca um cliente específico pelo ID.
    
    Args:
        conexao: Conexão com o banco
        cliente_id: ID do cliente
    
    Returns:
        Dados do cliente ou None
    """
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE id = ?", (cliente_id,))
        cliente = cursor.fetchone()
        return cliente
    except sqlite3.Error as erro:
        print(f"❌ Erro ao buscar cliente: {erro}")
        return None


def buscar_cliente_por_email(conexao, email: str):
    """
    Busca um cliente específico pelo email.
    
    Args:
        conexao: Conexão com o banco
        email: Email do cliente
    
    Returns:
        Dados do cliente ou None
    """
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE email = ?", (email,))
        cliente = cursor.fetchone()
        return cliente
    except sqlite3.Error as erro:
        print(f"❌ Erro ao buscar cliente: {erro}")
        return None


def atualizar_cliente(conexao, cliente_id: int, nome: str = None, 
                      email: str = None, telefone: str = None) -> bool:
    """
    Atualiza dados de um cliente.
    
    Args:
        conexao: Conexão com o banco
        cliente_id: ID do cliente
        nome: Novo nome (opcional)
        email: Novo email (opcional)
        telefone: Novo telefone (opcional)
    
    Returns:
        True se atualizado com sucesso
    """
    try:
        cursor = conexao.cursor()
        
        # Verificar se cliente existe
        cursor.execute("SELECT * FROM Clientes WHERE id = ?", (cliente_id,))
        if not cursor.fetchone():
            print(f"❌ Cliente com ID {cliente_id} não encontrado")
            return False
        
        # Construir SQL dinamicamente baseado nos campos a atualizar
        campos = []
        valores = []
        
        if nome is not None:
            campos.append("nome = ?")
            valores.append(nome)
        if email is not None:
            campos.append("email = ?")
            valores.append(email)
        if telefone is not None:
            campos.append("telefone = ?")
            valores.append(telefone)
        
        if not campos:
            print("⚠️  Nenhum campo para atualizar")
            return False
        
        valores.append(cliente_id)
        sql = f"UPDATE Clientes SET {', '.join(campos)} WHERE id = ?"
        
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"✓ Cliente ID {cliente_id} atualizado com sucesso")
        return True
        
    except sqlite3.IntegrityError:
        print(f"⚠️  Email já cadastrado por outro cliente")
        return False
    except sqlite3.Error as erro:
        print(f"❌ Erro ao atualizar cliente: {erro}")
        return False


def deletar_cliente(conexao, cliente_id: int) -> bool:
    """
    Deleta um cliente do banco.
    
    Args:
        conexao: Conexão com o banco
        cliente_id: ID do cliente
    
    Returns:
        True se deletado com sucesso
    """
    try:
        cursor = conexao.cursor()
        
        # Verificar se cliente existe
        cursor.execute("SELECT nome FROM Clientes WHERE id = ?", (cliente_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print(f"❌ Cliente com ID {cliente_id} não encontrado")
            return False
        
        nome_cliente = resultado[0]
        cursor.execute("DELETE FROM Clientes WHERE id = ?", (cliente_id,))
        conexao.commit()
        print(f"✓ Cliente '{nome_cliente}' (ID: {cliente_id}) deletado com sucesso")
        return True
        
    except sqlite3.Error as erro:
        print(f"❌ Erro ao deletar cliente: {erro}")
        return False


# ============================================================================
# FUNÇÕES DE EXIBIÇÃO
# ============================================================================

def exibir_clientes_tabela(clientes: List) -> None:
    """Exibe clientes em formato de tabela."""
    if not clientes:
        print("📭 Nenhum cliente cadastrado\n")
        return
    
    print("\n" + "=" * 100)
    print(f"{'ID':<5} {'Nome':<25} {'Email':<35} {'Telefone':<15} {'Data Cadastro':<15}")
    print("=" * 100)
    
    for cliente in clientes:
        id_cliente = cliente[0]
        nome = cliente[1]
        email = cliente[2]
        telefone = cliente[3] if cliente[3] else "N/A"
        data_cadastro = cliente[4]
        
        # Truncar texto se muito longo
        nome = nome[:22] + "..." if len(nome) > 25 else nome
        email = email[:32] + "..." if len(email) > 35 else email
        
        print(f"{id_cliente:<5} {nome:<25} {email:<35} {telefone:<15} {data_cadastro:<15}")
    
    print("=" * 100 + "\n")


def exibir_cliente_detalhado(cliente) -> None:
    """Exibe detalhes completos de um cliente."""
    if not cliente:
        print("❌ Cliente não encontrado\n")
        return
    
    print("\n" + "=" * 60)
    print(f"  DETALHES DO CLIENTE")
    print("=" * 60)
    print(f"\n📋 ID:              {cliente[0]}")
    print(f"👤 Nome:            {cliente[1]}")
    print(f"📧 Email:           {cliente[2]}")
    print(f"☎️  Telefone:        {cliente[3] if cliente[3] else 'Não informado'}")
    print(f"📅 Data Cadastro:   {cliente[4]}")
    print("\n" + "=" * 60 + "\n")


# ============================================================================
# EXEMPLOS DE USO
# ============================================================================

def exemplo_uso():
    """Demonstra o uso do sistema de banco de dados."""
    
    # Conectar ao banco
    conexao = conectar_banco()
    if not conexao:
        return
    
    # Criar tabela
    criar_tabela_clientes(conexao)
    
    print("=" * 70)
    print(" EXEMPLOS: SISTEMA DE BANCO DE DADOS COM SQLite")
    print("=" * 70 + "\n")
    
    # Exemplo 1: Inserir clientes
    print("--- Exemplo 1: Inserindo Clientes ---\n")
    clientes_novos = [
        ("Ana Silva", "ana.silva@email.com", "(11) 98765-4321"),
        ("Bruno Santos", "bruno.santos@email.com", "(21) 99876-5432"),
        ("Carla Oliveira", "carla.oliveira@email.com", "(31) 97654-3210"),
        ("Diego Costa", "diego.costa@email.com", "(41) 98765-0123"),
        ("Elaine Martins", "elaine.martins@email.com", "(51) 99876-1234"),
    ]
    
    for nome, email, telefone in clientes_novos:
        inserir_cliente(conexao, nome, email, telefone)
    
    print()
    
    # Exemplo 2: Listar todos os clientes
    print("--- Exemplo 2: Listando Todos os Clientes ---")
    clientes = listar_clientes(conexao)
    exibir_clientes_tabela(clientes)
    
    # Exemplo 3: Buscar cliente por ID
    print("--- Exemplo 3: Buscando Cliente por ID ---\n")
    cliente = buscar_cliente_por_id(conexao, 1)
    exibir_cliente_detalhado(cliente)
    
    # Exemplo 4: Buscar cliente por email
    print("--- Exemplo 4: Buscando Cliente por Email ---\n")
    cliente = buscar_cliente_por_email(conexao, "bruno.santos@email.com")
    exibir_cliente_detalhado(cliente)
    
    # Exemplo 5: Atualizar cliente
    print("--- Exemplo 5: Atualizando Cliente ---\n")
    atualizar_cliente(conexao, 2, telefone="(21) 99999-9999")
    cliente = buscar_cliente_por_id(conexao, 2)
    exibir_cliente_detalhado(cliente)
    
    # Exemplo 6: Tentar inserir email duplicado
    print("--- Exemplo 6: Tentando Inserir Email Duplicado ---\n")
    inserir_cliente(conexao, "Novo Nome", "ana.silva@email.com", "(99) 99999-9999")
    print()
    
    # Exemplo 7: Contar clientes
    print("--- Exemplo 7: Estatísticas ---\n")
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM Clientes")
    total = cursor.fetchone()[0]
    print(f"📊 Total de clientes: {total}\n")
    
    # Exemplo 8: Deletar cliente
    print("--- Exemplo 8: Deletando Cliente ---\n")
    deletar_cliente(conexao, 5)
    print()
    
    # Exemplo 9: Listar clientes atualizado
    print("--- Exemplo 9: Lista Atualizada Após Deleção ---")
    clientes = listar_clientes(conexao)
    exibir_clientes_tabela(clientes)
    
    # Exemplo 10: Buscar por padrão de nome
    print("--- Exemplo 10: Buscando Clientes com 'a' no Nome ---\n")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE nome LIKE '%a%'")
    clientes_filtrados = cursor.fetchall()
    exibir_clientes_tabela(clientes_filtrados)
    
    # Exemplo 11: Ordenar alfabeticamente
    print("--- Exemplo 11: Clientes Ordenados por Nome ---")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Clientes ORDER BY nome ASC")
    clientes_ordenados = cursor.fetchall()
    exibir_clientes_tabela(clientes_ordenados)
    
    # Fechar conexão
    conexao.close()
    print("✓ Conexão com banco de dados fechada\n")


# ============================================================================
# MENU INTERATIVO
# ============================================================================

def menu_principal():
    """Menu interativo para gerenciar clientes."""
    
    conexao = conectar_banco()
    if not conexao:
        return
    
    criar_tabela_clientes(conexao)
    
    while True:
        print("\n" + "=" * 50)
        print(" SISTEMA DE GERENCIAMENTO DE CLIENTES")
        print("=" * 50)
        print("\n1. Inserir novo cliente")
        print("2. Listar todos os clientes")
        print("3. Buscar cliente por ID")
        print("4. Buscar cliente por email")
        print("5. Atualizar cliente")
        print("6. Deletar cliente")
        print("7. Estatísticas")
        print("8. Ver exemplos de uso")
        print("0. Sair")
        print()
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print()
            nome = input("Nome do cliente: ").strip()
            email = input("Email: ").strip()
            telefone = input("Telefone (opcional): ").strip() or None
            
            if nome and email:
                inserir_cliente(conexao, nome, email, telefone)
            else:
                print("❌ Nome e email são obrigatórios")
        
        elif opcao == "2":
            clientes = listar_clientes(conexao)
            exibir_clientes_tabela(clientes)
        
        elif opcao == "3":
            print()
            try:
                cliente_id = int(input("ID do cliente: "))
                cliente = buscar_cliente_por_id(conexao, cliente_id)
                exibir_cliente_detalhado(cliente)
            except ValueError:
                print("❌ ID deve ser um número")
        
        elif opcao == "4":
            print()
            email = input("Email: ").strip()
            cliente = buscar_cliente_por_email(conexao, email)
            exibir_cliente_detalhado(cliente)
        
        elif opcao == "5":
            print()
            try:
                cliente_id = int(input("ID do cliente a atualizar: "))
                nome = input("Novo nome (deixe em branco para não alterar): ").strip() or None
                email = input("Novo email (deixe em branco para não alterar): ").strip() or None
                telefone = input("Novo telefone (deixe em branco para não alterar): ").strip() or None
                
                atualizar_cliente(conexao, cliente_id, nome, email, telefone)
            except ValueError:
                print("❌ ID deve ser um número")
        
        elif opcao == "6":
            print()
            try:
                cliente_id = int(input("ID do cliente a deletar: "))
                confirmacao = input(f"Tem certeza? (s/n): ").lower().strip()
                if confirmacao == "s":
                    deletar_cliente(conexao, cliente_id)
                else:
                    print("❌ Operação cancelada")
            except ValueError:
                print("❌ ID deve ser um número")
        
        elif opcao == "7":
            cursor = conexao.cursor()
            cursor.execute("SELECT COUNT(*) FROM Clientes")
            total = cursor.fetchone()[0]
            print(f"\n📊 Total de clientes: {total}\n")
        
        elif opcao == "8":
            print("\n⏭️  Executando exemplos...\n")
            conexao.close()
            exemplo_uso()
            conexao = conectar_banco()
        
        elif opcao == "0":
            print("\n👋 Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida")
    
    conexao.close()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    # Descomente a linha abaixo para ver os exemplos automaticamente
    exemplo_uso()
    
    # Descomente a linha abaixo para usar o menu interativo
    # menu_principal()
