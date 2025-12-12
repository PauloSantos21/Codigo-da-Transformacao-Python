import sqlite3
from datetime import datetime

class GerenciadorTarefas:
    """Sistema de Gerenciamento de Tarefas com SQLite"""
    
    def __init__(self, nome_banco='tarefas.db'):
        """
        Inicializa o gerenciador de tarefas
        
        Args:
            nome_banco: Nome do arquivo do banco de dados SQLite
        """
        self.nome_banco = nome_banco
        self.criar_tabela()
    
    def criar_tabela(self):
        """Cria a tabela de tarefas no banco de dados"""
        try:
            conexao = sqlite3.connect(self.nome_banco)
            cursor = conexao.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    status TEXT DEFAULT 'Pendente',
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_conclusao TIMESTAMP
                )
            ''')
            
            conexao.commit()
            conexao.close()
            print("✓ Tabela de tarefas criada/verificada com sucesso!")
        except sqlite3.Error as e:
            print(f"✗ Erro ao criar tabela: {e}")
    
    def adicionar_tarefa(self, titulo, descricao=''):
        """
        Adiciona uma nova tarefa ao banco de dados
        
        Args:
            titulo: Título da tarefa (obrigatório)
            descricao: Descrição da tarefa (opcional)
        
        Returns:
            bool: True se adicionado com sucesso, False caso contrário
        """
        if not titulo.strip():
            print("✗ O título da tarefa não pode estar vazio!")
            return False
        
        try:
            conexao = sqlite3.connect(self.nome_banco)
            cursor = conexao.cursor()
            
            cursor.execute('''
                INSERT INTO tarefas (titulo, descricao, status)
                VALUES (?, ?, ?)
            ''', (titulo, descricao, 'Pendente'))
            
            conexao.commit()
            tarefa_id = cursor.lastrowid
            conexao.close()
            
            print(f"✓ Tarefa #{tarefa_id} adicionada com sucesso!")
            print(f"  Título: {titulo}")
            if descricao:
                print(f"  Descrição: {descricao}")
            return True
        except sqlite3.Error as e:
            print(f"✗ Erro ao adicionar tarefa: {e}")
            return False
    
    def visualizar_tarefas(self, filtro_status=None):
        """
        Visualiza todas as tarefas ou filtra por status
        
        Args:
            filtro_status: Filtrar por status ('Pendente', 'Concluída', None para todas)
        
        Returns:
            list: Lista de tarefas
        """
        try:
            conexao = sqlite3.connect(self.nome_banco)
            conexao.row_factory = sqlite3.Row
            cursor = conexao.cursor()
            
            if filtro_status:
                cursor.execute('''
                    SELECT * FROM tarefas 
                    WHERE status = ?
                    ORDER BY data_criacao DESC
                ''', (filtro_status,))
            else:
                cursor.execute('''
                    SELECT * FROM tarefas 
                    ORDER BY data_criacao DESC
                ''')
            
            tarefas = cursor.fetchall()
            conexao.close()
            
            if not tarefas:
                print("✗ Nenhuma tarefa encontrada!")
                return []
            
            print("\n" + "="*80)
            print("TAREFAS".center(80))
            print("="*80)
            
            for tarefa in tarefas:
                print(f"\nID: {tarefa['id']}")
                print(f"Título: {tarefa['titulo']}")
                if tarefa['descricao']:
                    print(f"Descrição: {tarefa['descricao']}")
                print(f"Status: {tarefa['status']}")
                print(f"Data de Criação: {tarefa['data_criacao']}")
                if tarefa['data_conclusao']:
                    print(f"Data de Conclusão: {tarefa['data_conclusao']}")
                print("-" * 80)
            
            return list(tarefas)
        except sqlite3.Error as e:
            print(f"✗ Erro ao visualizar tarefas: {e}")
            return []
    
    def excluir_tarefa(self, tarefa_id):
        """
        Exclui uma tarefa pelo ID
        
        Args:
            tarefa_id: ID da tarefa a ser excluída
        
        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            conexao = sqlite3.connect(self.nome_banco)
            cursor = conexao.cursor()
            
            # Verifica se a tarefa existe
            cursor.execute('SELECT titulo FROM tarefas WHERE id = ?', (tarefa_id,))
            tarefa = cursor.fetchone()
            
            if not tarefa:
                print(f"✗ Tarefa #{tarefa_id} não encontrada!")
                conexao.close()
                return False
            
            # Exclui a tarefa
            cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
            conexao.commit()
            conexao.close()
            
            print(f"✓ Tarefa #{tarefa_id} '{tarefa[0]}' excluída com sucesso!")
            return True
        except sqlite3.Error as e:
            print(f"✗ Erro ao excluir tarefa: {e}")
            return False
    
    def marcar_como_concluida(self, tarefa_id):
        """
        Marca uma tarefa como concluída
        
        Args:
            tarefa_id: ID da tarefa
        
        Returns:
            bool: True se marcado com sucesso, False caso contrário
        """
        try:
            conexao = sqlite3.connect(self.nome_banco)
            cursor = conexao.cursor()
            
            cursor.execute('SELECT titulo FROM tarefas WHERE id = ?', (tarefa_id,))
            tarefa = cursor.fetchone()
            
            if not tarefa:
                print(f"✗ Tarefa #{tarefa_id} não encontrada!")
                conexao.close()
                return False
            
            cursor.execute('''
                UPDATE tarefas 
                SET status = ?, data_conclusao = ?
                WHERE id = ?
            ''', ('Concluída', datetime.now(), tarefa_id))
            
            conexao.commit()
            conexao.close()
            
            print(f"✓ Tarefa #{tarefa_id} marcada como concluída!")
            return True
        except sqlite3.Error as e:
            print(f"✗ Erro ao atualizar tarefa: {e}")
            return False
    
    def obter_estatisticas(self):
        """
        Retorna estatísticas das tarefas
        
        Returns:
            dict: Dicionário com estatísticas
        """
        try:
            conexao = sqlite3.connect(self.nome_banco)
            cursor = conexao.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM tarefas')
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tarefas WHERE status = 'Pendente'")
            pendentes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tarefas WHERE status = 'Concluída'")
            concluidas = cursor.fetchone()[0]
            
            conexao.close()
            
            return {
                'total': total,
                'pendentes': pendentes,
                'concluidas': concluidas
            }
        except sqlite3.Error as e:
            print(f"✗ Erro ao obter estatísticas: {e}")
            return {}


def menu_principal(gerenciador):
    """
    Exibe o menu principal do sistema
    
    Args:
        gerenciador: Instância do GerenciadorTarefas
    """
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE GERENCIAMENTO DE TAREFAS".center(50))
        print("="*50)
        
        # Estatísticas
        stats = gerenciador.obter_estatisticas()
        print(f"\n📊 Estatísticas:")
        print(f"   Total: {stats['total']} | Pendentes: {stats['pendentes']} | Concluídas: {stats['concluidas']}")
        
        print("\n1. Adicionar Tarefa")
        print("2. Visualizar Todas as Tarefas")
        print("3. Visualizar Tarefas Pendentes")
        print("4. Visualizar Tarefas Concluídas")
        print("5. Marcar Tarefa como Concluída")
        print("6. Excluir Tarefa")
        print("7. Sair")
        print("="*50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            print("\n--- ADICIONAR NOVA TAREFA ---")
            titulo = input("Título da tarefa: ").strip()
            descricao = input("Descrição (opcional): ").strip()
            gerenciador.adicionar_tarefa(titulo, descricao)
        
        elif opcao == '2':
            gerenciador.visualizar_tarefas()
        
        elif opcao == '3':
            gerenciador.visualizar_tarefas(filtro_status='Pendente')
        
        elif opcao == '4':
            gerenciador.visualizar_tarefas(filtro_status='Concluída')
        
        elif opcao == '5':
            try:
                tarefa_id = int(input("\nID da tarefa a marcar como concluída: "))
                gerenciador.marcar_como_concluida(tarefa_id)
            except ValueError:
                print("✗ ID inválido! Digite um número inteiro.")
        
        elif opcao == '6':
            try:
                tarefa_id = int(input("\nID da tarefa a excluir: "))
                confirmacao = input(f"Tem certeza que deseja excluir? (s/n): ").strip().lower()
                if confirmacao == 's':
                    gerenciador.excluir_tarefa(tarefa_id)
            except ValueError:
                print("✗ ID inválido! Digite um número inteiro.")
        
        elif opcao == '7':
            print("\n✓ Encerrando o sistema. Até logo!")
            break
        
        else:
            print("✗ Opção inválida! Tente novamente.")


if __name__ == '__main__':
    # Cria uma instância do gerenciador
    gerenciador = GerenciadorTarefas('tarefas.db')
    
    # Inicia o menu principal
    menu_principal(gerenciador)