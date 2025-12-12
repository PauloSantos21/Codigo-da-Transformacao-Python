import requests # type: ignore
from datetime import datetime
from typing import Optional, Dict, Any, List


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# API Open Library (SEM NECESSIDADE DE AUTENTICAÇÃO)
# Documentação: https://openlibrary.org/developers/api
OPEN_LIBRARY_API = "https://openlibrary.org/search.json"


# ============================================================================
# CLASSE PARA ESTRUTURAR DADOS DE FILMES
# ============================================================================

class Filme:
    """Classe que representa um filme."""
    
    def __init__(self, titulo: str, generos: list, sinopse: str, 
                 ano: int = None, rating: float = 0, popularidade: float = 0,
                 poster: str = None, id_filme: int = None):
        """
        Inicializa um filme.
        
        Args:
            titulo: Título do filme
            generos: Lista de gêneros
            sinopse: Sinopse/descrição
            ano: Ano de lançamento
            rating: Avaliação (0-10)
            popularidade: Índice de popularidade
            poster: URL do poster
            id_filme: ID no TMDB
        """
        self.titulo = titulo
        self.generos = generos
        self.sinopse = sinopse
        self.ano = ano
        self.rating = rating
        self.popularidade = popularidade
        self.poster = poster
        self.id_filme = id_filme
    
    def __str__(self):
        generos_str = ", ".join(self.generos) if self.generos else "N/A"
        return f"{self.titulo} ({self.ano}) - {generos_str} ⭐ {self.rating}"
    
    def __repr__(self):
        return f"Filme(titulo='{self.titulo}', ano={self.ano}, rating={self.rating})"


# ============================================================================
# DADOS DE EXEMPLO (para teste sem API)
# ============================================================================

FILMES_EXEMPLO = [
    Filme(
        "Inception",
        ["Ficção Científica", "Ação", "Thriller"],
        "Um ladrão que rouba segredos corporativos através da tecnologia de compartilhamento de sonhos é dado a tarefa inversa de implantar uma ideia.",
        2010, 8.8, 28.5
    ),
    Filme(
        "The Shawshank Redemption",
        ["Drama"],
        "Dois homens presos formam uma amizade duradoura enquanto buscam uma redenção final.",
        1994, 9.3, 26.4
    ),
    Filme(
        "The Dark Knight",
        ["Ação", "Crime", "Drama"],
        "Quando a ameaça conhecida como o Coringa surge da his gelatinosa do crime de Gotham, ele causa caos e anarquia.",
        2008, 9.0, 29.3
    ),
    Filme(
        "Pulp Fiction",
        ["Crime", "Drama"],
        "As vidas de dois assassinos de aluguel, um boxeador, uma esposa de gângster e um par de bandidos se entrelaçam.",
        1994, 8.9, 25.2
    ),
    Filme(
        "Forrest Gump",
        ["Drama", "Romance"],
        "A vida é como uma caixa de chocolates, você nunca sabe o que vai conseguir. A história de um homem simples.",
        1994, 8.8, 24.1
    ),
    Filme(
        "Interstellar",
        ["Ficção Científica", "Drama"],
        "Um grupo de exploradores viaja através de um buraco de minhoca no espaço para garantir a sobrevivência da humanidade.",
        2014, 8.6, 27.8
    ),
    Filme(
        "Fight Club",
        ["Drama"],
        "Um homem insone que trabalha em um departamento de reclamações encontra alívio em grupos de apoio fictícios.",
        1999, 8.8, 26.0
    ),
    Filme(
        "The Matrix",
        ["Ação", "Ficção Científica"],
        "Um hacker descobre a verdade sobre sua realidade e seu papel no conflito com seus criadores.",
        1999, 8.7, 25.5
    ),
]

# Gêneros únicos
GENEROS_DISPONIVEIS = set()
for filme in FILMES_EXEMPLO:
    GENEROS_DISPONIVEIS.update(filme.generos)
GENEROS_DISPONIVEIS = sorted(list(GENEROS_DISPONIVEIS))


# ============================================================================
# FUNÇÕES DE BUSCA E CONSUMO DE API
# ============================================================================

def buscar_filme_tmdb(nome_filme: str) -> List[Filme]:
    """
    Busca filmes na API Open Library (SEM CHAVE NECESSÁRIA).
    
    Args:
        nome_filme: Nome do filme/livro a buscar
    
    Returns:
        Lista de filmes encontrados
    """
    try:
        parametros = {
            "title": nome_filme,
            "limit": 5
        }
        
        print(f"🔍 Buscando '{nome_filme}' na Open Library...")
        resposta = requests.get(OPEN_LIBRARY_API, params=parametros, timeout=10)
        
        if resposta.status_code != 200:
            print(f"❌ Erro na API: {resposta.status_code}")
            return buscar_filme_exemplo(nome_filme)
        
        dados = resposta.json()
        filmes = []
        
        for doc in dados.get("docs", [])[:5]:
            # Extrair dados do Open Library
            titulo = doc.get("title", "Desconhecido")
            autores = doc.get("author_name", [])
            generos = doc.get("subject", [])[:3]  # Pega até 3 gêneros
            sinopse = doc.get("first_sentence", ["Sinopse não disponível"])[0] if doc.get("first_sentence") else "Sinopse não disponível"
            ano = doc.get("first_publish_year", None)
            rating = doc.get("ratings_average", 0)
            
            filme = Filme(
                titulo=titulo,
                generos=generos,
                sinopse=sinopse,
                ano=ano,
                rating=rating if rating else 0,
                popularidade=0
            )
            filmes.append(filme)
        
        print(f"✓ {len(filmes)} resultado(s) encontrado(s)!\n")
        return filmes
    
    except Exception as erro:
        print(f"❌ Erro: {erro}")
        print("📖 Usando base de dados local de exemplo...\n")
        return buscar_filme_exemplo(nome_filme)


def buscar_filme_exemplo(nome_filme: str) -> List[Filme]:
    """
    Busca filmes nos dados de exemplo.
    
    Args:
        nome_filme: Nome do filme a buscar
    
    Returns:
        Lista de filmes encontrados
    """
    nome_lower = nome_filme.lower()
    return [f for f in FILMES_EXEMPLO if nome_lower in f.titulo.lower()]


def filtrar_por_genero(filmes: List[Filme], genero: str) -> List[Filme]:
    """Filtra filmes por gênero."""
    genero_lower = genero.lower()
    return [f for f in filmes if any(genero_lower in g.lower() for g in f.generos)]


def filtrar_por_rating(filmes: List[Filme], rating_min: float) -> List[Filme]:
    """Filtra filmes por rating mínimo."""
    return [f for f in filmes if f.rating >= rating_min]


def ordenar_por_rating(filmes: List[Filme], decrescente: bool = True) -> List[Filme]:
    """Ordena filmes por rating."""
    return sorted(filmes, key=lambda f: f.rating, reverse=decrescente)


def ordenar_por_ano(filmes: List[Filme], decrescente: bool = True) -> List[Filme]:
    """Ordena filmes por ano."""
    return sorted(filmes, key=lambda f: f.ano if f.ano else 0, reverse=decrescente)


# ============================================================================
# FUNÇÕES DE EXIBIÇÃO
# ============================================================================

def exibir_filme_completo(filme: Filme) -> None:
    """Exibe informações completas de um filme."""
    print("\n" + "=" * 70)
    print(f"  {filme.titulo.upper()}")
    print("=" * 70)
    
    print(f"\n📅 Ano de lançamento: {filme.ano if filme.ano else 'N/A'}")
    print(f"⭐ Avaliação: {filme.rating}/10")
    print(f"📊 Popularidade: {filme.popularidade:.1f}")
    
    if filme.generos:
        generos_str = " | ".join(filme.generos)
        print(f"🎬 Gêneros: {generos_str}")
    
    print(f"\n📝 Sinopse:")
    print(f"{filme.sinopse[:300]}..." if len(filme.sinopse) > 300 else f"{filme.sinopse}")
    
    print("\n" + "=" * 70 + "\n")


def exibir_filme_resumido(filme: Filme) -> None:
    """Exibe resumo de um filme."""
    generos_str = ", ".join(filme.generos) if filme.generos else "N/A"
    print(f"• {filme.titulo} ({filme.ano})")
    print(f"  Gêneros: {generos_str}")
    print(f"  Rating: ⭐ {filme.rating}/10")
    print(f"  Sinopse: {filme.sinopse[:80]}...\n")


def exibir_lista_tabela(filmes: List[Filme]) -> None:
    """Exibe filmes em formato de tabela."""
    if not filmes:
        print("❌ Nenhum filme encontrado.\n")
        return
    
    print("\n" + "=" * 85)
    print(f"{'Título':<35} {'Ano':<8} {'Rating':<10} {'Gêneros':<30}")
    print("=" * 85)
    
    for filme in filmes:
        generos = ", ".join(filme.generos[:2]) if filme.generos else "N/A"
        titulo_truncado = filme.titulo[:32] + "..." if len(filme.titulo) > 32 else filme.titulo
        
        print(f"{titulo_truncado:<35} {str(filme.ano):<8} {filme.rating:>6.1f}/10  {generos:<30}")
    
    print("=" * 85 + "\n")


def exibir_apenas_titulo_sinopse(filme: Filme) -> None:
    """Exibe apenas título e sinopse."""
    print(f"\n📽️ {filme.titulo} ({filme.ano})")
    print(f"Sinopse: {filme.sinopse}\n")


def exibir_apenas_titulo_genero(filme: Filme) -> None:
    """Exibe apenas título e gênero."""
    generos = " | ".join(filme.generos) if filme.generos else "Gênero desconhecido"
    print(f"🎬 {filme.titulo} - {generos}")


# ============================================================================
# ESTATÍSTICAS
# ============================================================================

def calcular_rating_medio(filmes: List[Filme]) -> float:
    """Calcula rating médio dos filmes."""
    if not filmes:
        return 0
    return sum(f.rating for f in filmes) / len(filmes)


def filme_melhor_avaliado(filmes: List[Filme]) -> Optional[Filme]:
    """Retorna o filme melhor avaliado."""
    return max(filmes, key=lambda f: f.rating) if filmes else None


def filme_pior_avaliado(filmes: List[Filme]) -> Optional[Filme]:
    """Retorna o filme pior avaliado."""
    return min(filmes, key=lambda f: f.rating) if filmes else None


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

def exemplo_uso():
    """Demonstra o uso do programa."""
    
    print("\n" + "=" * 70)
    print(" EXEMPLOS: BUSCADOR DE FILMES/LIVROS (API Open Library)")
    print("=" * 70 + "\n")
    
    # Exemplo 1: Listar todos os filmes locais
    print("--- Exemplo 1: Filmes Locais (Base de Dados) ---")
    exibir_lista_tabela(FILMES_EXEMPLO)
    
    # Exemplo 2: Buscar na API Open Library
    print("--- Exemplo 2: Buscar 'Harry Potter' na API ---")
    filmes_api = buscar_filme_tmdb("Harry Potter")
    exibir_lista_tabela(filmes_api)
    
    # Exemplo 3: Buscar outro filme
    print("--- Exemplo 3: Buscar 'Lord of the Rings' ---")
    filmes_api2 = buscar_filme_tmdb("Lord of the Rings")
    exibir_lista_tabela(filmes_api2)
    
    # Exemplo 4: Buscar um filme local
    print("--- Exemplo 4: Buscar 'Inception' (Local) ---")
    filmes_encontrados = buscar_filme_exemplo("Inception")
    exibir_lista_tabela(filmes_encontrados)
    
    # Exemplo 5: Exibir filme completo
    print("--- Exemplo 5: Detalhes Completos ---")
    if filmes_encontrados:
        exibir_filme_completo(filmes_encontrados[0])
    
    # Exemplo 6: Apenas título e sinopse
    print("--- Exemplo 6: Título e Sinopse ---")
    for filme in FILMES_EXEMPLO[:2]:
        exibir_apenas_titulo_sinopse(filme)
    
    # Exemplo 7: Apenas título e gênero
    print("--- Exemplo 7: Título e Gênero ---")
    for filme in FILMES_EXEMPLO[:3]:
        exibir_apenas_titulo_genero(filme)
    
    # Exemplo 8: Filtrar por gênero
    print("--- Exemplo 8: Filmes de Ficção Científica ---")
    ficcion_cientifica = filtrar_por_genero(FILMES_EXEMPLO, "Ficção Científica")
    exibir_lista_tabela(ficcion_cientifica)
    
    # Exemplo 9: Filtrar por rating
    print("--- Exemplo 9: Filmes com Rating ≥ 8.8 ---")
    top_rated = filtrar_por_rating(FILMES_EXEMPLO, 8.8)
    exibir_lista_tabela(top_rated)
    
    # Exemplo 10: Ordenar por rating
    print("--- Exemplo 10: Filmes Ordenados por Rating ---")
    ordenados = ordenar_por_rating(FILMES_EXEMPLO)
    exibir_lista_tabela(ordenados)
    
    # Exemplo 11: Estatísticas
    print("--- Exemplo 11: Estatísticas ---")
    melhor = filme_melhor_avaliado(FILMES_EXEMPLO)
    pior = filme_pior_avaliado(FILMES_EXEMPLO)
    media = calcular_rating_medio(FILMES_EXEMPLO)
    
    print(f"\n📊 Estatísticas de {len(FILMES_EXEMPLO)} filmes:")
    print(f"  ⭐ Melhor avaliado: {melhor.titulo} ({melhor.rating}/10)")
    print(f"  ⭐ Pior avaliado: {pior.titulo} ({pior.rating}/10)")
    print(f"  📈 Rating médio: {media:.2f}/10\n")


def menu_interativo():
    """Menu interativo."""
    
    print("\n" + "=" * 70)
    print(" BUSCADOR DE FILMES - MENU INTERATIVO")
    print("=" * 70)
    
    while True:
        print("\n1. Buscar filme por nome")
        print("2. Listar todos os filmes")
        print("3. Filtrar por gênero")
        print("4. Ver filmes por rating")
        print("5. Ver detalhes completos de um filme")
        print("6. Ver estatísticas")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            nome = input("Digite o nome do filme: ").strip()
            filmes = buscar_filme_exemplo(nome)
            exibir_lista_tabela(filmes)
        
        elif opcao == "2":
            exibir_lista_tabela(FILMES_EXEMPLO)
        
        elif opcao == "3":
            print(f"\nGêneros disponíveis: {', '.join(GENEROS_DISPONIVEIS)}")
            genero = input("Digite o gênero: ").strip()
            filmes = filtrar_por_genero(FILMES_EXEMPLO, genero)
            exibir_lista_tabela(filmes)
        
        elif opcao == "4":
            try:
                rating = float(input("Rating mínimo (0-10): "))
                filmes = filtrar_por_rating(FILMES_EXEMPLO, rating)
                ordenados = ordenar_por_rating(filmes)
                exibir_lista_tabela(ordenados)
            except ValueError:
                print("❌ Valor inválido!")
        
        elif opcao == "5":
            nome = input("Digite o nome do filme: ").strip()
            filmes = buscar_filme_exemplo(nome)
            if filmes:
                exibir_filme_completo(filmes[0])
            else:
                print("❌ Filme não encontrado!\n")
        
        elif opcao == "6":
            melhor = filme_melhor_avaliado(FILMES_EXEMPLO)
            pior = filme_pior_avaliado(FILMES_EXEMPLO)
            media = calcular_rating_medio(FILMES_EXEMPLO)
            
            print(f"\n📊 Estatísticas:")
            print(f"  Total de filmes: {len(FILMES_EXEMPLO)}")
            print(f"  ⭐ Melhor: {melhor.titulo} ({melhor.rating}/10)")
            print(f"  ⭐ Pior: {pior.titulo} ({pior.rating}/10)")
            print(f"  📈 Média: {media:.2f}/10\n")
        
        elif opcao == "7":
            print("Encerrando...")
            break
        
        else:
            print("❌ Opção inválida!")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    exemplo_uso()
    
    # Descomente para menu interativo
    # resposta = input("Deseja usar o menu interativo? (s/n): ").strip().lower()
    # if resposta == "s":
    #     menu_interativo()