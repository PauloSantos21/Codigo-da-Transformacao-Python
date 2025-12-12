from datetime import datetime, timedelta


class Livro:
    """Classe que representa um livro na biblioteca."""
    
    def __init__(self, titulo, autor, isbn, ano_publicacao):
        """
        Inicializa um objeto Livro.
        
        Args:
            titulo (str): Título do livro
            autor (str): Autor do livro
            isbn (str): ISBN único do livro
            ano_publicacao (int): Ano de publicação
        """
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao
        self.disponivel = True
        self.emprestado_para = None
        self.data_emprestimo = None
    
    def __str__(self):
        """Representação em string do livro."""
        status = "Disponível" if self.disponivel else f"Emprestado para {self.emprestado_para}"
        return f"{self.titulo} - {self.autor} ({self.ano_publicacao}) [ISBN: {self.isbn}] - {status}"
    
    def __repr__(self):
        """Representação técnica do livro."""
        return f"Livro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"
    
    def emprestar(self, nome_pessoa):
        """
        Marca o livro como emprestado.
        
        Args:
            nome_pessoa (str): Nome da pessoa que está pegando o livro
        """
        if self.disponivel:
            self.disponivel = False
            self.emprestado_para = nome_pessoa
            self.data_emprestimo = datetime.now()
            return True
        return False
    
    def devolver(self):
        """Marca o livro como devolvido."""
        if not self.disponivel:
            self.disponivel = True
            self.emprestado_para = None
            self.data_emprestimo = None
            return True
        return False


class Biblioteca:
    """Classe que gerencia uma coleção de livros e empréstimos."""
    
    def __init__(self, nome):
        """
        Inicializa uma biblioteca.
        
        Args:
            nome (str): Nome da biblioteca
        """
        self.nome = nome
        self.livros = []
    
    def __str__(self):
        """Representação em string da biblioteca."""
        return f"Biblioteca '{self.nome}' com {len(self.livros)} livros"
    
    def adicionar_livro(self, livro):
        """
        Adiciona um livro à biblioteca.
        
        Args:
            livro (Livro): Objeto Livro a adicionar
        
        Returns:
            bool: True se adicionado, False se ISBN já existe
        """
        # Verificar se ISBN já existe
        if any(l.isbn == livro.isbn for l in self.livros):
            print(f"❌ Erro: Livro com ISBN {livro.isbn} já existe na biblioteca!")
            return False
        
        self.livros.append(livro)
        print(f"✓ Livro '{livro.titulo}' adicionado com sucesso!")
        return True
    
    def remover_livro(self, isbn):
        """
        Remove um livro da biblioteca pelo ISBN.
        
        Args:
            isbn (str): ISBN do livro a remover
        
        Returns:
            bool: True se removido, False caso contrário
        """
        for livro in self.livros:
            if livro.isbn == isbn:
                if not livro.disponivel:
                    print(f"❌ Erro: Não é possível remover '{livro.titulo}' - está emprestado!")
                    return False
                self.livros.remove(livro)
                print(f"✓ Livro '{livro.titulo}' removido com sucesso!")
                return True
        
        print(f"❌ Erro: Livro com ISBN {isbn} não encontrado!")
        return False
    
    def pesquisar_por_titulo(self, titulo):
        """
        Pesquisa livros por título (busca parcial).
        
        Args:
            titulo (str): Parte do título a buscar
        
        Returns:
            list: Lista de livros encontrados
        """
        return [l for l in self.livros if titulo.lower() in l.titulo.lower()]
    
    def pesquisar_por_autor(self, autor):
        """
        Pesquisa livros por autor.
        
        Args:
            autor (str): Nome do autor
        
        Returns:
            list: Lista de livros do autor
        """
        return [l for l in self.livros if autor.lower() in l.autor.lower()]
    
    def emprestar_livro(self, isbn, nome_pessoa):
        """
        Empresta um livro para uma pessoa.
        
        Args:
            isbn (str): ISBN do livro
            nome_pessoa (str): Nome da pessoa
        
        Returns:
            bool: True se emprestado, False caso contrário
        """
        for livro in self.livros:
            if livro.isbn == isbn:
                if livro.emprestar(nome_pessoa):
                    print(f"✓ Livro '{livro.titulo}' emprestado para {nome_pessoa}!")
                    return True
                else:
                    print(f"❌ Erro: '{livro.titulo}' não está disponível!")
                    return False
        
        print(f"❌ Erro: Livro com ISBN {isbn} não encontrado!")
        return False
    
    def devolver_livro(self, isbn):
        """
        Registra a devolução de um livro.
        
        Args:
            isbn (str): ISBN do livro
        
        Returns:
            bool: True se devolvido, False caso contrário
        """
        for livro in self.livros:
            if livro.isbn == isbn:
                if livro.devolver():
                    print(f"✓ Livro '{livro.titulo}' devolvido com sucesso!")
                    return True
                else:
                    print(f"❌ Erro: '{livro.titulo}' já está disponível!")
                    return False
        
        print(f"❌ Erro: Livro com ISBN {isbn} não encontrado!")
        return False
    
    def listar_disponveis(self):
        """Lista todos os livros disponíveis."""
        disponiveis = [l for l in self.livros if l.disponivel]
        
        if not disponiveis:
            print("\n📚 Nenhum livro disponível no momento.\n")
            return
        
        print(f"\n📚 LIVROS DISPONÍVEIS ({len(disponiveis)}):")
        print("=" * 80)
        for i, livro in enumerate(disponiveis, 1):
            print(f"{i}. {livro}")
        print("=" * 80 + "\n")
    
    def listar_emprestados(self):
        """Lista todos os livros emprestados."""
        emprestados = [l for l in self.livros if not l.disponivel]
        
        if not emprestados:
            print("\n📖 Nenhum livro emprestado no momento.\n")
            return
        
        print(f"\n📖 LIVROS EMPRESTADOS ({len(emprestados)}):")
        print("=" * 80)
        for i, livro in enumerate(emprestados, 1):
            dias = (datetime.now() - livro.data_emprestimo).days
            print(f"{i}. {livro} - Emprestado há {dias} dias")
        print("=" * 80 + "\n")
    
    def listar_todos(self):
        """Lista todos os livros da biblioteca."""
        if not self.livros:
            print("\n📚 A biblioteca está vazia.\n")
            return
        
        print(f"\n📚 ACERVO DA BIBLIOTECA ({len(self.livros)} livros):")
        print("=" * 80)
        for i, livro in enumerate(self.livros, 1):
            print(f"{i}. {livro}")
        print("=" * 80 + "\n")
    
    def obter_estatisticas(self):
        """Retorna estatísticas da biblioteca."""
        total = len(self.livros)
        disponivel = sum(1 for l in self.livros if l.disponivel)
        emprestados = total - disponivel
        
        return {
            "total": total,
            "disponivel": disponivel,
            "emprestados": emprestados
        }


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print(" SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
    print("=" * 80 + "\n")
    
    # Criar uma biblioteca
    biblioteca = Biblioteca("Biblioteca Municipal")
    
    # Criar alguns livros
    livro1 = Livro("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "978-8532630759", 1943)
    livro2 = Livro("1984", "George Orwell", "978-8535902778", 1949)
    livro3 = Livro("Dom Casmurro", "Machado de Assis", "978-8509023456", 1899)
    livro4 = Livro("O Cortiço", "Aluísio Azevedo", "978-8509076543", 1890)
    livro5 = Livro("Orgulho e Preconceito", "Jane Austen", "978-8572326247", 1813)
    livro6 = Livro("O Hobbit", "J.R.R. Tolkien", "978-8533613370", 1937)
    
    # Adicionar livros à biblioteca
    print("--- ADICIONANDO LIVROS À BIBLIOTECA ---\n")
    for livro in [livro1, livro2, livro3, livro4, livro5, livro6]:
        biblioteca.adicionar_livro(livro)
    
    # Listar todos os livros
    biblioteca.listar_todos()
    
    # Emprestar alguns livros
    print("--- EMPRESTANDO LIVROS ---\n")
    biblioteca.emprestar_livro("978-8532630759", "João Silva")
    biblioteca.emprestar_livro("978-8535902778", "Maria Santos")
    biblioteca.emprestar_livro("978-8509023456", "Carlos Oliveira")
    
    # Listar livros disponíveis e emprestados
    print("\n--- STATUS ATUAL DA BIBLIOTECA ---")
    biblioteca.listar_disponveis()
    biblioteca.listar_emprestados()
    
    # Pesquisar livros
    print("--- PESQUISAS ---\n")
    print("Livros de Machado de Assis:")
    for livro in biblioteca.pesquisar_por_autor("Machado"):
        print(f"  - {livro}")
    
    print("\nLivros com 'Príncipe' no título:")
    for livro in biblioteca.pesquisar_por_titulo("Príncipe"):
        print(f"  - {livro}")
    
    # Devolver um livro
    print("\n--- DEVOLVENDO LIVRO ---\n")
    biblioteca.devolver_livro("978-8532630759")
    
    # Estatísticas
    print("--- ESTATÍSTICAS DA BIBLIOTECA ---\n")
    stats = biblioteca.obter_estatisticas()
    print(f"Total de livros: {stats['total']}")
    print(f"Livros disponíveis: {stats['disponivel']}")
    print(f"Livros emprestados: {stats['emprestados']}")
    
    # Listar novamente
    print("\n--- STATUS APÓS DEVOLUÇÃO ---")
    biblioteca.listar_disponveis()