import sqlite3
from datetime import datetime
from typing import List, Tuple
import re


# ============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================================

BANCO_DADOS = "clientes_filtro.db"


class FiltroSQL:
    """Classe para executar filtros e consultas SQL avançadas."""
    
    def __init__(self, nome_banco: str = BANCO_DADOS):
        """Inicializa o gerenciador de filtros."""
        self.nome_banco = nome_banco
        self.conexao = None
    
    def conectar(self) -> bool:
        """Estabelece conexão com o banco."""
        try:
            self.conexao = sqlite3.connect(self.nome_banco)
            self.conexao.row_factory = sqlite3.Row
            print(f"✓ Conectado ao banco: {self.nome_banco}\n")
            return True
        except sqlite3.Error as erro:
            print(f"❌ Erro: {erro}")
            return False
    
    def desconectar(self) -> None:
        """Fecha a conexão."""
        if self.conexao:
            self.conexao.close()
            print("✓ Conexão fechada\n")
    
    def criar_tabela_com_dados(self) -> None:
        """Cria tabela e insere dados de exemplo."""
        try:
            cursor = self.conexao.cursor()
            
            # Criar tabela
            sql_criar = """
            CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefone TEXT,
                cidade TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ativo BOOLEAN DEFAULT 1
            )
            """
            cursor.execute(sql_criar)
            
            # Limpar dados antigos
            cursor.execute("DELETE FROM Clientes")
            
            # Inserir dados de exemplo
            clientes = [
                ("Ana Silva", "ana.silva@email.com", "(11) 98765-4321", "São Paulo", 1),
                ("Anderson Santos", "anderson@email.com", "(11) 99876-5432", "São Paulo", 1),
                ("Alice Costa", "alice.costa@email.com", "(21) 97654-3210", "Rio de Janeiro", 1),
                ("Bruno Oliveira", "bruno.oliveira@email.com", "(21) 98765-0123", "Rio de Janeiro", 1),
                ("Brenda Souza", "brenda.souza@email.com", "(31) 99876-1234", "Belo Horizonte", 0),
                ("Carla Martins", "carla.martins@email.com", "(41) 97654-5678", "Curitiba", 1),
                ("Carlos Costa", "carlos.costa@email.com", "(41) 98765-6789", "Curitiba", 1),
                ("Daniela Rocha", "daniela.rocha@email.com", "(51) 99876-7890", "Porto Alegre", 1),
                ("David Ferreira", "david.ferreira@email.com", "(51) 97654-8901", "Porto Alegre", 0),
                ("Elaine Gomes", "elaine.gomes@email.com", "(61) 98765-9012", "Brasília", 1),
                ("Eduardo Lima", "eduardo.lima@email.com", "(61) 99876-0123", "Brasília", 1),
                ("Fernanda Alves", "fernanda.alves@email.com", "(71) 97654-1234", "Salvador", 1),
                ("Felipe Ribeiro", "felipe.ribeiro@email.com", "(71) 98765-2345", "Salvador", 0),
                ("Gabriela Pereira", "gabriela.pereira@email.com", "(81) 99876-3456", "Recife", 1),
                ("Gabriel Barbosa", "gabriel.barbosa@email.com", "(81) 97654-4567", "Recife", 1),
            ]
            
            sql_insert = "INSERT INTO Clientes (nome, email, telefone, cidade, ativo) VALUES (?, ?, ?, ?, ?)"
            cursor.executemany(sql_insert, clientes)
            
            self.conexao.commit()
            print(f"✓ Tabela criada com {len(clientes)} clientes de exemplo\n")
        
        except sqlite3.Error as erro:
            print(f"❌ Erro: {erro}")
    
    def executar_consulta(self, sql: str, parametros: tuple = None) -> List:
        """Executa uma consulta SQL e retorna os resultados."""
        try:
            cursor = self.conexao.cursor()
            if parametros:
                cursor.execute(sql, parametros)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as erro:
            print(f"❌ Erro na consulta: {erro}")
            return []
    
    # ========================================================================
    # FILTROS COM WHERE
    # ========================================================================
    
    def nomes_comecam_com(self, letra: str) -> List:
        """Filtra clientes cujo nome começa com uma letra específica."""
        sql = "SELECT * FROM Clientes WHERE nome LIKE ? ORDER BY nome"
        return self.executar_consulta(sql, (f"{letra}%",))
    
    def nome_contem(self, texto: str) -> List:
        """Filtra clientes que têm um texto no nome."""
        sql = "SELECT * FROM Clientes WHERE nome LIKE ? ORDER BY nome"
        return self.executar_consulta(sql, (f"%{texto}%",))
    
    def email_dominio(self, dominio: str) -> List:
        """Filtra clientes por domínio de email."""
        sql = "SELECT * FROM Clientes WHERE email LIKE ? ORDER BY nome"
        return self.executar_consulta(sql, (f"%{dominio}%",))
    
    def por_cidade(self, cidade: str) -> List:
        """Filtra clientes por cidade."""
        sql = "SELECT * FROM Clientes WHERE cidade = ? ORDER BY nome"
        return self.executar_consulta(sql, (cidade,))
    
    def ativos_apenas(self) -> List:
        """Retorna apenas clientes ativos."""
        sql = "SELECT * FROM Clientes WHERE ativo = 1 ORDER BY nome"
        return self.executar_consulta(sql)
    
    def inativos_apenas(self) -> List:
        """Retorna apenas clientes inativos."""
        sql = "SELECT * FROM Clientes WHERE ativo = 0 ORDER BY nome"
        return self.executar_consulta(sql)
    
    def multiplos_criterios(self, cidade: str = None, ativo: int = None) -> List:
        """Filtra com múltiplos critérios (AND)."""
        sql = "SELECT * FROM Clientes WHERE 1=1"
        parametros = []
        
        if cidade:
            sql += " AND cidade = ?"
            parametros.append(cidade)
        
        if ativo is not None:
            sql += " AND ativo = ?"
            parametros.append(ativo)
        
        sql += " ORDER BY nome"
        return self.executar_consulta(sql, tuple(parametros) if parametros else None)
    
    # ========================================================================
    # FILTROS COM OR, IN, BETWEEN
    # ========================================================================
    
    def cidades_multiplas(self, cidades: list) -> List:
        """Filtra clientes de múltiplas cidades (IN)."""
        placeholders = ",".join("?" * len(cidades))
        sql = f"SELECT * FROM Clientes WHERE cidade IN ({placeholders}) ORDER BY cidade, nome"
        return self.executar_consulta(sql, tuple(cidades))
    
    def nomes_ou_cidades(self, letra: str, cidade: str) -> List:
        """Filtra clientes: nome começa com letra OU são de uma cidade (OR)."""
        sql = "SELECT * FROM Clientes WHERE nome LIKE ? OR cidade = ? ORDER BY nome"
        return self.executar_consulta(sql, (f"{letra}%", cidade))
    
    # ========================================================================
    # AGREGAÇÃO E AGRUPAMENTO
    # ========================================================================
    
    def contar_por_cidade(self) -> List:
        """Conta clientes por cidade."""
        sql = """
        SELECT cidade, COUNT(*) as total, SUM(CASE WHEN ativo=1 THEN 1 ELSE 0 END) as ativos
        FROM Clientes
        GROUP BY cidade
        ORDER BY total DESC
        """
        return self.executar_consulta(sql)
    
    def contar_por_letra_inicial(self) -> List:
        """Conta clientes por letra inicial do nome."""
        sql = """
        SELECT SUBSTR(nome, 1, 1) as letra, COUNT(*) as total
        FROM Clientes
        GROUP BY SUBSTR(nome, 1, 1)
        ORDER BY letra
        """
        return self.executar_consulta(sql)
    
    def cidades_com_mais_clientes(self, minimo: int = 1) -> List:
        """Retorna cidades com pelo menos N clientes."""
        sql = """
        SELECT cidade, COUNT(*) as total
        FROM Clientes
        GROUP BY cidade
        HAVING COUNT(*) >= ?
        ORDER BY total DESC
        """
        return self.executar_consulta(sql, (minimo,))
    
    def letra_inicial_com_contagem(self, letra: str) -> int:
        """Conta quantos clientes começam com uma letra."""
        sql = "SELECT COUNT(*) FROM Clientes WHERE nome LIKE ?"
        resultado = self.executar_consulta(sql, (f"{letra}%",))
        return resultado[0][0] if resultado else 0
    
    # ========================================================================
    # ORDENAÇÃO
    # ========================================================================
    
    def ordenar_nome_asc(self) -> List:
        """Ordena por nome (A-Z)."""
        sql = "SELECT * FROM Clientes ORDER BY nome ASC"
        return self.executar_consulta(sql)
    
    def ordenar_nome_desc(self) -> List:
        """Ordena por nome (Z-A)."""
        sql = "SELECT * FROM Clientes ORDER BY nome DESC"
        return self.executar_consulta(sql)
    
    def ordenar_cidade_depois_nome(self) -> List:
        """Ordena por cidade e depois por nome."""
        sql = "SELECT * FROM Clientes ORDER BY cidade ASC, nome ASC"
        return self.executar_consulta(sql)
    
    def ordenar_recentes_primeiro(self) -> List:
        """Ordena pelos clientes cadastrados mais recentemente."""
        sql = "SELECT * FROM Clientes ORDER BY data_cadastro DESC"
        return self.executar_consulta(sql)
    
    # ========================================================================
    # BUSCAS AVANÇADAS
    # ========================================================================
    
    def comprimento_nome(self, minimo: int = 1) -> List:
        """Filtra clientes por comprimento do nome."""
        sql = """
        SELECT *, LENGTH(nome) as comprimento
        FROM Clientes
        WHERE LENGTH(nome) >= ?
        ORDER BY comprimento DESC
        """
        return self.executar_consulta(sql, (minimo,))
    
    def nomes_duplicados_iniciais(self) -> List:
        """Encontra clientes com mesma letra inicial."""
        sql = """
        SELECT 
            SUBSTR(nome, 1, 1) as letra,
            nome,
            COUNT(*) OVER (PARTITION BY SUBSTR(nome, 1, 1)) as total_mesma_letra
        FROM Clientes
        ORDER BY letra, nome
        """
        return self.executar_consulta(sql)
    
    def sem_telefone(self) -> List:
        """Retorna clientes sem telefone cadastrado."""
        sql = "SELECT * FROM Clientes WHERE telefone IS NULL ORDER BY nome"
        return self.executar_consulta(sql)
    
    def com_telefone(self) -> List:
        """Retorna clientes com telefone cadastrado."""
        sql = "SELECT * FROM Clientes WHERE telefone IS NOT NULL ORDER BY nome"
        return self.executar_consulta(sql)
    
    # ========================================================================
    # ESTATÍSTICAS
    # ========================================================================
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas gerais."""
        try:
            cursor = self.conexao.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM Clientes")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Clientes WHERE ativo = 1")
            ativos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Clientes WHERE telefone IS NOT NULL")
            com_telefone = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT cidade) FROM Clientes")
            total_cidades = cursor.fetchone()[0]
            
            return {
                "total": total,
                "ativos": ativos,
                "inativos": total - ativos,
                "com_telefone": com_telefone,
                "sem_telefone": total - com_telefone,
                "total_cidades": total_cidades
            }
        except sqlite3.Error:
            return {}


# ============================================================================
# FUNÇÕES DE EXIBIÇÃO
# ============================================================================

def exibir_tabela(clientes: List, titulo: str = "RESULTADOS") -> None:
    """Exibe clientes em formato de tabela."""
    if not clientes:
        print("📭 Nenhum resultado encontrado\n")
        return
    
    print("\n" + "=" * 120)
    print(f"  {titulo} ({len(clientes)} resultado(s))")
    print("=" * 120)
    
    # Cabeçalho
    print(f"{'ID':<4} {'Nome':<25} {'Email':<30} {'Telefone':<15} {'Cidade':<18} {'Ativo':<6}")
    print("=" * 120)
    
    # Dados
    for cliente in clientes:
        id_c = cliente[0]
        nome = cliente[1][:22] + "..." if len(cliente[1]) > 25 else cliente[1]
        email = cliente[2][:27] + "..." if len(cliente[2]) > 30 else cliente[2]
        telefone = cliente[3] if cliente[3] else "N/A"
        cidade = cliente[4][:15] + "..." if len(cliente[4]) > 18 else cliente[4]
        ativo = "✓ Sim" if cliente[6] else "✗ Não"
        
        print(f"{id_c:<4} {nome:<25} {email:<30} {telefone:<15} {cidade:<18} {ativo:<6}")
    
    print("=" * 120 + "\n")


def exibir_resultado_contagem(resultado: List, titulo: str) -> None:
    """Exibe resultado de contagem."""
    print("\n" + "=" * 60)
    print(f"  {titulo}")
    print("=" * 60)
    
    if not resultado:
        print("Nenhum resultado")
    else:
        for row in resultado:
            print(f"  {row[0]:<20}: {row[1]}")
    
    print("=" * 60 + "\n")


# ============================================================================
# EXEMPLOS PRÁTICOS
# ============================================================================

def exemplo_filtros_completo():
    """Demonstra todos os tipos de filtros."""
    
    filtro = FiltroSQL()
    
    if not filtro.conectar():
        return
    
    filtro.criar_tabela_com_dados()
    
    print("=" * 70)
    print(" EXEMPLOS: FILTROS SQL AVANÇADOS")
    print("=" * 70 + "\n")
    
    # ====== 1. WHERE com LIKE (começa com) ======
    print("--- 1. Clientes cujo nome COMEÇA COM 'A' ---")
    clientes = filtro.nomes_comecam_com("A")
    exibir_tabela(clientes, f"NOMES COMEÇANDO COM 'A'")
    
    # ====== 2. WHERE com LIKE (contém) ======
    print("--- 2. Clientes com 'ana' NO NOME ---")
    clientes = filtro.nome_contem("ana")
    exibir_tabela(clientes, "NOMES CONTENDO 'ANA'")
    
    # ====== 3. Filtro por Domínio de Email ======
    print("--- 3. Clientes com EMAIL @email.com ---")
    clientes = filtro.email_dominio("@email.com")
    exibir_tabela(clientes, "EMAIL @email.com")
    
    # ====== 4. Filtro por Cidade ======
    print("--- 4. Clientes de SÃO PAULO ---")
    clientes = filtro.por_cidade("São Paulo")
    exibir_tabela(clientes, "CLIENTES DE SÃO PAULO")
    
    # ====== 5. Apenas Ativos ======
    print("--- 5. Apenas CLIENTES ATIVOS ---")
    clientes = filtro.ativos_apenas()
    exibir_tabela(clientes, "CLIENTES ATIVOS")
    
    # ====== 6. Apenas Inativos ======
    print("--- 6. Apenas CLIENTES INATIVOS ---")
    clientes = filtro.inativos_apenas()
    exibir_tabela(clientes, "CLIENTES INATIVOS")
    
    # ====== 7. Múltiplos Critérios (AND) ======
    print("--- 7. ATIVOS em São Paulo (AND) ---")
    clientes = filtro.multiplos_criterios(cidade="São Paulo", ativo=1)
    exibir_tabela(clientes, "ATIVOS EM SÃO PAULO")
    
    # ====== 8. IN (múltiplas cidades) ======
    print("--- 8. Clientes de SP, RJ ou MG (IN) ---")
    clientes = filtro.cidades_multiplas(["São Paulo", "Rio de Janeiro", "Belo Horizonte"])
    exibir_tabela(clientes, "CLIENTES DE SP, RJ OU MG")
    
    # ====== 9. OR (nome começa com A OU cidade = RJ) ======
    print("--- 9. Nome começa com 'B' OU moram no Rio (OR) ---")
    clientes = filtro.nomes_ou_cidades("B", "Rio de Janeiro")
    exibir_tabela(clientes, "NOME COM 'B' OU RIO DE JANEIRO")
    
    # ====== 10. Contagem por Cidade ======
    print("--- 10. CONTAGEM POR CIDADE ---")
    resultado = filtro.contar_por_cidade()
    exibir_resultado_contagem(resultado, "CLIENTES POR CIDADE")
    
    # ====== 11. Contagem por Letra Inicial ======
    print("--- 11. CONTAGEM POR LETRA INICIAL ---")
    resultado = filtro.contar_por_letra_inicial()
    exibir_resultado_contagem(resultado, "CLIENTES POR LETRA INICIAL")
    
    # ====== 12. Cidades com Mínimo de Clientes ======
    print("--- 12. Cidades com MÍNIMO 2 clientes ---")
    resultado = filtro.cidades_com_mais_clientes(2)
    exibir_resultado_contagem(resultado, "CIDADES COM 2+ CLIENTES")
    
    # ====== 13. Ordenação Alfabética ======
    print("--- 13. Clientes ORDENADOS por NOME (A-Z) ---")
    clientes = filtro.ordenar_nome_asc()
    exibir_tabela(clientes, "ORDEM ALFABÉTICA (A-Z)")
    
    # ====== 14. Ordenação Reversa ======
    print("--- 14. Clientes ORDENADOS por NOME (Z-A) ---")
    clientes = filtro.ordenar_nome_desc()
    exibir_tabela(clientes, "ORDEM ALFABÉTICA (Z-A)")
    
    # ====== 15. Ordenação por Cidade + Nome ======
    print("--- 15. Clientes ORDENADOS por CIDADE depois NOME ---")
    clientes = filtro.ordenar_cidade_depois_nome()
    exibir_tabela(clientes, "ORDENADO: CIDADE > NOME")
    
    # ====== 16. Comprimento do Nome ======
    print("--- 16. Clientes com NOME COMPRIDO (15+ caracteres) ---")
    clientes = filtro.comprimento_nome(15)
    exibir_tabela(clientes, "NOMES COMPRIDOS (15+)")
    
    # ====== 17. Sem Telefone ======
    print("--- 17. Clientes SEM TELEFONE ---")
    clientes = filtro.sem_telefone()
    exibir_tabela(clientes, "SEM TELEFONE")
    
    # ====== 18. Com Telefone ======
    print("--- 18. Clientes COM TELEFONE ---")
    clientes = filtro.com_telefone()
    exibir_tabela(clientes, "COM TELEFONE")
    
    # ====== 19. Estatísticas ======
    print("--- 19. ESTATÍSTICAS GERAIS ---")
    stats = filtro.obter_estatisticas()
    print("\n" + "=" * 60)
    print(f"  ESTATÍSTICAS DO BANCO")
    print("=" * 60)
    print(f"  Total de clientes:     {stats['total']}")
    print(f"  Ativos:                {stats['ativos']}")
    print(f"  Inativos:              {stats['inativos']}")
    print(f"  Com telefone:          {stats['com_telefone']}")
    print(f"  Sem telefone:          {stats['sem_telefone']}")
    print(f"  Total de cidades:      {stats['total_cidades']}")
    print("=" * 60 + "\n")
    
    # ====== 20. Letra Inicial com Contagem ======
    print("--- 20. CONTAGEM DE CLIENTES POR LETRA INICIAL ---\n")
    for letra in "ABCDEFGHIJ":
        total = filtro.letra_inicial_com_contagem(letra)
        if total > 0:
            print(f"  {letra}: {total} cliente(s)")
    print()
    
    filtro.desconectar()


def menu_filtro_interativo():
    """Menu para filtrar dados interativamente."""
    
    filtro = FiltroSQL()
    
    if not filtro.conectar():
        return
    
    filtro.criar_tabela_com_dados()
    
    while True:
        print("\n" + "=" * 50)
        print(" MENU DE FILTROS SQL")
        print("=" * 50)
        print("\n1. Clientes por letra inicial")
        print("2. Clientes por cidade")
        print("3. Apenas ativos")
        print("4. Apenas inativos")
        print("5. Cidades com múltiplos clientes")
        print("6. Estatísticas")
        print("7. Ordena por nome (A-Z)")
        print("8. Ver exemplos completos")
        print("0. Sair\n")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            letra = input("\nLetra inicial: ").strip().upper()[0]
            clientes = filtro.nomes_comecam_com(letra)
            exibir_tabela(clientes, f"NOMES COMEÇANDO COM '{letra}'")
        
        elif opcao == "2":
            cidade = input("\nCidade: ").strip()
            clientes = filtro.por_cidade(cidade)
            exibir_tabela(clientes, f"CLIENTES DE {cidade.upper()}")
        
        elif opcao == "3":
            clientes = filtro.ativos_apenas()
            exibir_tabela(clientes, "CLIENTES ATIVOS")
        
        elif opcao == "4":
            clientes = filtro.inativos_apenas()
            exibir_tabela(clientes, "CLIENTES INATIVOS")
        
        elif opcao == "5":
            resultado = filtro.contar_por_cidade()
            exibir_resultado_contagem(resultado, "CLIENTES POR CIDADE")
        
        elif opcao == "6":
            stats = filtro.obter_estatisticas()
            print(f"\n📊 Total: {stats['total']} | Ativos: {stats['ativos']} | Cidades: {stats['total_cidades']}\n")
        
        elif opcao == "7":
            clientes = filtro.ordenar_nome_asc()
            exibir_tabela(clientes, "CLIENTES (A-Z)")
        
        elif opcao == "8":
            exemplo_filtros_completo()
            filtro.conectar()
            filtro.criar_tabela_com_dados()
        
        elif opcao == "0":
            print("\n👋 Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida\n")
    
    filtro.desconectar()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    # Executar exemplos
    exemplo_filtros_completo()
    
    # Descomente abaixo para menu interativo
    # menu_filtro_interativo()