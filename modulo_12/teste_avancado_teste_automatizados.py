"""
Exemplo de Teste Avançado com pytest e Flask
Module: Testes Automatizados

Este arquivo demonstra padrões avançados de teste incluindo:
- Fixtures com escopos diferentes
- Parametrização
- Mocking e patches
- Testes com marcadores
- Captura de erros
"""

import pytest
import json
from pathlib import Path
import sys

# Importar a API
sys.path.insert(0, str(Path(__file__).parent.parent / 'modulo_13'))
from modulo_13.crie_api_para_blog_dev_api_com_flask import create_app
from config_servidor_dev_api_com_flask import TestingConfig


# ============================================================================
# FIXTURES COM DIFERENTES ESCOPOS
# ============================================================================

@pytest.fixture(scope="session")
def app_session():
    """Fixture de escopo de sessão - criada uma vez por sessão de testes"""
    app = create_app()
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture(scope="module")
def app_module():
    """Fixture de escopo de módulo - criada uma vez por módulo"""
    app = create_app()
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture(scope="function")
def app_function():
    """Fixture de escopo de função - criada uma vez por teste (padrão)"""
    app = create_app()
    app.config.from_object(TestingConfig)
    yield app
    # Cleanup (se necessário)


@pytest.fixture
def client_with_posts(client):
    """Fixture que fornece um cliente com posts pré-carregados"""
    posts = [
        {'title': 'Post 1', 'content': 'Conteúdo 1', 'author': 'Autor 1'},
        {'title': 'Post 2', 'content': 'Conteúdo 2', 'author': 'Autor 2'},
        {'title': 'Post 3', 'content': 'Conteúdo 3', 'author': 'Autor 3'},
    ]
    
    for post in posts:
        client.post('/api/posts',
                   data=json.dumps(post),
                   content_type='application/json')
    
    return client


# ============================================================================
# TESTES COM PARAMETRIZAÇÃO
# ============================================================================

class TestParametrization:
    """Demonstra como usar parametrização para reduzir duplicação"""
    
    @pytest.mark.parametrize("title,content,author", [
        ("Python Basics", "Aprenda Python", "Maria"),
        ("Flask Tutorial", "Guia do Flask", "João"),
        ("API Design", "Design de APIs", "Ana"),
    ])
    def test_create_multiple_posts(self, client, title, content, author):
        """Testa criação de múltiplos posts com dados diferentes"""
        post = {'title': title, 'content': content, 'author': author}
        response = client.post('/api/posts',
                             data=json.dumps(post),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == title
        assert data['author'] == author
    
    @pytest.mark.parametrize("status_code,expected_error", [
        (400, "required"),  # Teste com título vazio
        (400, "required"),  # Teste com conteúdo vazio
    ])
    @pytest.mark.parametrize("missing_field", ["title", "content"])
    def test_invalid_post_creation(self, client, missing_field, status_code, expected_error):
        """Testa criação com campos obrigatórios faltando"""
        post = {'title': 'Título', 'content': 'Conteúdo'}
        del post[missing_field]
        
        response = client.post('/api/posts',
                             data=json.dumps(post),
                             content_type='application/json')
        
        assert response.status_code == status_code
    
    @pytest.mark.parametrize("search_term,expected_count", [
        ("Python", 2),
        ("Flask", 1),
        ("NonExistent", 0),
    ])
    def test_search_with_different_terms(self, client, search_term, expected_count):
        """Testa busca com diferentes termos"""
        # Criar posts
        posts = [
            {'title': 'Python Basics', 'content': 'Content'},
            {'title': 'Python Advanced', 'content': 'Content'},
            {'title': 'Flask Guide', 'content': 'Content'},
        ]
        
        for post in posts:
            client.post('/api/posts',
                       data=json.dumps(post),
                       content_type='application/json')
        
        # Buscar
        response = client.get(f'/api/posts/search?q={search_term}')
        data = json.loads(response.data)
        
        assert len(data) == expected_count


# ============================================================================
# TESTES COM MARCADORES CUSTOMIZADOS
# ============================================================================

class TestMarkedTests:
    """Testes com marcadores para filtrar e organizar"""
    
    @pytest.mark.unit
    def test_post_creation_unit(self, client, sample_post):
        """Teste unitário de criação de post"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        assert response.status_code == 201
    
    @pytest.mark.integration
    def test_post_full_workflow_integration(self, client, sample_post):
        """Teste de integração com fluxo completo"""
        # Criar
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Obter
        get_response = client.get(f'/api/posts/{post_id}')
        
        # Deletar
        delete_response = client.delete(f'/api/posts/{post_id}')
        
        assert create_response.status_code == 201
        assert get_response.status_code == 200
        assert delete_response.status_code == 200
    
    @pytest.mark.slow
    def test_bulk_operations(self, client):
        """Teste lento com muitas operações"""
        # Criar 100 posts
        for i in range(100):
            post = {
                'title': f'Post {i}',
                'content': f'Conteúdo {i}',
                'author': f'Autor {i}'
            }
            response = client.post('/api/posts',
                                 data=json.dumps(post),
                                 content_type='application/json')
            assert response.status_code == 201
        
        # Listar todos
        response = client.get('/api/posts')
        data = json.loads(response.data)
        assert len(data) == 100


# ============================================================================
# TESTES COM CAPTURA DE EXCEÇÕES
# ============================================================================

class TestExceptionHandling:
    """Testes para verificar tratamento de exceções"""
    
    def test_invalid_json_captured(self, client):
        """Testa captura de JSON inválido"""
        with pytest.raises(Exception):
            response = client.post('/api/posts',
                                 data='{invalid json}',
                                 content_type='application/json')
            # Força um erro se status for 400
            if response.status_code == 400:
                raise ValueError("JSON inválido recebido")
    
    def test_response_has_error_field_on_failure(self, client):
        """Verifica se erro contém campo 'error'"""
        response = client.post('/api/posts',
                             data=json.dumps({'title': ''}),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert 'error' in data
        assert isinstance(data['error'], str)
        assert len(data['error']) > 0


# ============================================================================
# TESTES COM FIXTURES MAIS COMPLEXAS
# ============================================================================

@pytest.fixture
def populated_api(client):
    """Fixture que popula a API com dados de teste"""
    posts_data = [
        {
            'title': 'Introdução ao Python',
            'content': 'Python é uma linguagem versátil',
            'author': 'Maria Silva'
        },
        {
            'title': 'Flask para Iniciantes',
            'content': 'Framework web poderoso',
            'author': 'João Santos'
        },
        {
            'title': 'Testes com pytest',
            'content': 'Aprenda a testar seu código',
            'author': 'Ana Costa'
        },
    ]
    
    created_ids = []
    for post_data in posts_data:
        response = client.post('/api/posts',
                             data=json.dumps(post_data),
                             content_type='application/json')
        created_ids.append(json.loads(response.data)['id'])
    
    yield client, created_ids
    
    # Cleanup: deletar todos os posts criados
    for post_id in created_ids:
        try:
            client.delete(f'/api/posts/{post_id}')
        except:
            pass


class TestWithPopulatedAPI:
    """Testes usando uma API pré-populada"""
    
    def test_search_in_populated_api(self, populated_api):
        """Testa busca em API com dados"""
        client, _ = populated_api
        
        response = client.get('/api/posts/search?q=Python')
        data = json.loads(response.data)
        
        assert len(data) == 1
        assert 'Python' in data[0]['title']
    
    def test_list_populated_api(self, populated_api):
        """Testa listagem em API com dados"""
        client, created_ids = populated_api
        
        response = client.get('/api/posts')
        data = json.loads(response.data)
        
        assert len(data) == len(created_ids)
    
    def test_update_in_populated_api(self, populated_api):
        """Testa atualização em API com dados"""
        client, created_ids = populated_api
        
        # Atualizar primeiro post
        update_data = {'title': 'Título Atualizado'}
        response = client.put(f'/api/posts/{created_ids[0]}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Título Atualizado'


# ============================================================================
# TESTES COM VERIFICAÇÃO DE ESTRUTURA
# ============================================================================

class TestResponseStructure:
    """Testes para verificar estrutura das respostas"""
    
    def test_post_response_structure(self, client, sample_post):
        """Verifica estrutura completa da resposta"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        # Verificar tipos
        assert isinstance(data['id'], int)
        assert isinstance(data['title'], str)
        assert isinstance(data['content'], str)
        assert isinstance(data['author'], str)
        assert isinstance(data['created_at'], str)
        assert isinstance(data['updated_at'], str)
        
        # Verificar valores não vazios
        assert data['id'] > 0
        assert len(data['title']) > 0
        assert len(data['content']) > 0
        assert len(data['author']) > 0
    
    def test_list_response_is_array(self, client, sample_post):
        """Verifica se listagem retorna array"""
        # Criar um post
        client.post('/api/posts',
                   data=json.dumps(sample_post),
                   content_type='application/json')
        
        response = client.get('/api/posts')
        data = json.loads(response.data)
        
        assert isinstance(data, list)
        if len(data) > 0:
            assert isinstance(data[0], dict)
            assert 'id' in data[0]
            assert 'title' in data[0]


# ============================================================================
# TESTES DE PERFORMANCE
# ============================================================================

class TestPerformance:
    """Testes básicos de performance"""
    
    def test_list_posts_response_time(self, client_with_posts):
        """Verifica tempo de resposta da listagem"""
        import time
        
        start_time = time.time()
        response = client_with_posts.get('/api/posts')
        end_time = time.time()
        
        elapsed_time = (end_time - start_time) * 1000  # em ms
        
        assert response.status_code == 200
        assert elapsed_time < 100  # Menos de 100ms
    
    def test_search_response_time(self, client_with_posts):
        """Verifica tempo de resposta da busca"""
        import time
        
        start_time = time.time()
        response = client_with_posts.get('/api/posts/search?q=Post')
        end_time = time.time()
        
        elapsed_time = (end_time - start_time) * 1000  # em ms
        
        assert response.status_code == 200
        assert elapsed_time < 100  # Menos de 100ms


if __name__ == '__main__':
    # Para rodar este arquivo individualmente
    pytest.main([__file__, '-v', '--tb=short'])