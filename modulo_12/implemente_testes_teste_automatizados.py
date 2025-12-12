"""
Testes Automatizados para API Flask com pytest
Module: Testes Automatizados
Author: Código da Transformação

Este módulo implementa uma suite completa de testes para a API Flask
usando o framework pytest, incluindo testes unitários, de integração,
fixtures, mocks e validações.

Para executar os testes:
    pytest implemente_testes_teste_automatizados.py -v
    pytest implemente_testes_teste_automatizados.py -v --cov
    pytest implemente_testes_teste_automatizados.py -v -s  # com prints
"""

import pytest
import json
import sys
from pathlib import Path
from datetime import datetime

# Adicionar o diretório modulo_13 ao path para importar a API
sys.path.insert(0, str(Path(__file__).parent.parent / 'modulo_13'))

from modulo_13.crie_api_para_blog_dev_api_com_flask import create_app
from config_servidor_dev_api_com_flask import TestingConfig


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def app():
    """Fixture que cria a aplicação Flask para testes"""
    app = create_app()
    app.config.from_object(TestingConfig)
    
    yield app
    
    # Cleanup (executado após cada teste)


@pytest.fixture
def client(app):
    """Fixture que cria um cliente de teste"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture para usar o CLI runner da Flask"""
    return app.test_cli_runner()


@pytest.fixture
def sample_post():
    """Fixture com dados de um post exemplo"""
    return {
        'title': 'Meu Primeiro Post',
        'content': 'Este é o conteúdo do meu primeiro post',
        'author': 'João Silva'
    }


@pytest.fixture
def multiple_posts():
    """Fixture com múltiplos posts"""
    return [
        {
            'title': 'Python Basics',
            'content': 'Introdução ao Python',
            'author': 'Maria'
        },
        {
            'title': 'Flask Tutorial',
            'content': 'Aprenda Flask do zero',
            'author': 'Carlos'
        },
        {
            'title': 'REST APIs',
            'content': 'Como criar APIs RESTful',
            'author': 'Ana'
        }
    ]


# ============================================================================
# TESTES DE SAÚDE DA API
# ============================================================================

class TestHealthCheck:
    """Testes para verificar a saúde da API"""
    
    def test_health_endpoint_returns_200(self, client):
        """Testa se o endpoint de saúde retorna status 200"""
        response = client.get('/api/health')
        assert response.status_code == 200
    
    def test_health_endpoint_returns_healthy_status(self, client):
        """Testa se a resposta contém status 'healthy'"""
        response = client.get('/api/health')
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_health_endpoint_includes_timestamp(self, client):
        """Testa se a resposta inclui timestamp"""
        response = client.get('/api/health')
        data = json.loads(response.data)
        assert 'timestamp' in data
        # Validar formato ISO
        assert 'T' in data['timestamp']


# ============================================================================
# TESTES DE LISTAGEM DE POSTS
# ============================================================================

class TestListPosts:
    """Testes para listar posts"""
    
    def test_list_posts_returns_200(self, client):
        """Testa se listar posts retorna status 200"""
        response = client.get('/api/posts')
        assert response.status_code == 200
    
    def test_list_posts_returns_empty_list_initially(self, client):
        """Testa se inicialmente retorna lista vazia"""
        response = client.get('/api/posts')
        data = json.loads(response.data)
        assert data == []
        assert isinstance(data, list)
    
    def test_list_posts_returns_json(self, client):
        """Testa se a resposta é JSON válido"""
        response = client.get('/api/posts')
        assert response.content_type == 'application/json'
    
    def test_list_posts_after_creation(self, client, sample_post):
        """Testa se posts criados aparecem na lista"""
        # Criar um post
        client.post('/api/posts', 
                   data=json.dumps(sample_post),
                   content_type='application/json')
        
        # Listar posts
        response = client.get('/api/posts')
        data = json.loads(response.data)
        
        assert len(data) == 1
        assert data[0]['title'] == sample_post['title']


# ============================================================================
# TESTES DE CRIAÇÃO DE POSTS
# ============================================================================

class TestCreatePost:
    """Testes para criar novos posts"""
    
    def test_create_post_returns_201(self, client, sample_post):
        """Testa se criar post retorna status 201 (Created)"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        assert response.status_code == 201
    
    def test_create_post_returns_post_data(self, client, sample_post):
        """Testa se a resposta contém os dados do post criado"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert data['title'] == sample_post['title']
        assert data['content'] == sample_post['content']
        assert data['author'] == sample_post['author']
    
    def test_create_post_assigns_id(self, client, sample_post):
        """Testa se o post criado recebe um ID único"""
        response1 = client.post('/api/posts',
                              data=json.dumps(sample_post),
                              content_type='application/json')
        data1 = json.loads(response1.data)
        
        response2 = client.post('/api/posts',
                              data=json.dumps(sample_post),
                              content_type='application/json')
        data2 = json.loads(response2.data)
        
        assert 'id' in data1
        assert 'id' in data2
        assert data1['id'] != data2['id']
    
    def test_create_post_includes_timestamps(self, client, sample_post):
        """Testa se o post inclui created_at e updated_at"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert 'created_at' in data
        assert 'updated_at' in data
    
    def test_create_post_without_title_returns_400(self, client):
        """Testa se falta de título retorna erro 400"""
        invalid_post = {'content': 'Conteúdo sem título'}
        response = client.post('/api/posts',
                             data=json.dumps(invalid_post),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_create_post_without_content_returns_400(self, client):
        """Testa se falta de conteúdo retorna erro 400"""
        invalid_post = {'title': 'Título sem conteúdo'}
        response = client.post('/api/posts',
                             data=json.dumps(invalid_post),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_create_post_with_empty_title_returns_400(self, client):
        """Testa se título vazio retorna erro 400"""
        invalid_post = {'title': '', 'content': 'Conteúdo'}
        response = client.post('/api/posts',
                             data=json.dumps(invalid_post),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_create_post_without_json_returns_400(self, client):
        """Testa se dados não-JSON retornam erro 400"""
        response = client.post('/api/posts',
                             data='dados inválidos',
                             content_type='text/plain')
        assert response.status_code == 400
    
    def test_create_post_with_default_author(self, client):
        """Testa se author padrão é 'Anonymous' quando não fornecido"""
        post = {'title': 'Teste', 'content': 'Conteúdo'}
        response = client.post('/api/posts',
                             data=json.dumps(post),
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert data['author'] == 'Anonymous'


# ============================================================================
# TESTES DE OBTENÇÃO DE POST
# ============================================================================

class TestGetPost:
    """Testes para obter um post específico"""
    
    def test_get_existing_post_returns_200(self, client, sample_post):
        """Testa se obter post existente retorna 200"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Obter post
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 200
    
    def test_get_nonexistent_post_returns_404(self, client):
        """Testa se obter post inexistente retorna 404"""
        response = client.get('/api/posts/9999')
        assert response.status_code == 404
    
    def test_get_post_returns_correct_data(self, client, sample_post):
        """Testa se os dados retornados estão corretos"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        created_post = json.loads(create_response.data)
        post_id = created_post['id']
        
        # Obter post
        response = client.get(f'/api/posts/{post_id}')
        data = json.loads(response.data)
        
        assert data['title'] == sample_post['title']
        assert data['content'] == sample_post['content']
        assert data['id'] == post_id
    
    def test_get_post_error_message(self, client):
        """Testa se a mensagem de erro está correta"""
        response = client.get('/api/posts/999')
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Post not found'


# ============================================================================
# TESTES DE ATUALIZAÇÃO DE POSTS
# ============================================================================

class TestUpdatePost:
    """Testes para atualizar posts"""
    
    def test_update_post_returns_200(self, client, sample_post):
        """Testa se atualizar post retorna 200"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Atualizar post
        update_data = {'title': 'Título Atualizado'}
        response = client.put(f'/api/posts/{post_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
    
    def test_update_nonexistent_post_returns_404(self, client):
        """Testa se atualizar post inexistente retorna 404"""
        update_data = {'title': 'Novo Título'}
        response = client.put('/api/posts/9999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 404
    
    def test_update_post_title(self, client, sample_post):
        """Testa atualização de título"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Atualizar título
        new_title = 'Título Completamente Novo'
        update_data = {'title': new_title}
        response = client.put(f'/api/posts/{post_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        data = json.loads(response.data)
        
        assert data['title'] == new_title
    
    def test_update_post_content(self, client, sample_post):
        """Testa atualização de conteúdo"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Atualizar conteúdo
        new_content = 'Novo conteúdo do post'
        update_data = {'content': new_content}
        response = client.put(f'/api/posts/{post_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        data = json.loads(response.data)
        
        assert data['content'] == new_content
    
    def test_update_post_multiple_fields(self, client, sample_post):
        """Testa atualização de múltiplos campos"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Atualizar múltiplos campos
        update_data = {
            'title': 'Novo Título',
            'content': 'Novo Conteúdo',
            'author': 'Novo Autor'
        }
        response = client.put(f'/api/posts/{post_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        data = json.loads(response.data)
        
        assert data['title'] == update_data['title']
        assert data['content'] == update_data['content']
        assert data['author'] == update_data['author']
    
    def test_update_post_updates_timestamp(self, client, sample_post):
        """Testa se updated_at é atualizado"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        created_post = json.loads(create_response.data)
        original_updated_at = created_post['updated_at']
        post_id = created_post['id']
        
        # Aguardar um momento para garantir timestamps diferentes
        import time
        time.sleep(0.01)
        
        # Atualizar post
        update_data = {'title': 'Título Atualizado'}
        response = client.put(f'/api/posts/{post_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        updated_post = json.loads(response.data)
        
        assert updated_post['updated_at'] != original_updated_at


# ============================================================================
# TESTES DE DELEÇÃO DE POSTS
# ============================================================================

class TestDeletePost:
    """Testes para deletar posts"""
    
    def test_delete_post_returns_200(self, client, sample_post):
        """Testa se deletar post retorna 200"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Deletar post
        response = client.delete(f'/api/posts/{post_id}')
        assert response.status_code == 200
    
    def test_delete_nonexistent_post_returns_404(self, client):
        """Testa se deletar post inexistente retorna 404"""
        response = client.delete('/api/posts/9999')
        assert response.status_code == 404
    
    def test_delete_post_removes_from_list(self, client, sample_post):
        """Testa se post é realmente removido"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Deletar post
        client.delete(f'/api/posts/{post_id}')
        
        # Tentar obter post deletado
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 404
    
    def test_delete_post_success_message(self, client, sample_post):
        """Testa se a mensagem de sucesso está correta"""
        # Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        post_id = json.loads(create_response.data)['id']
        
        # Deletar post
        response = client.delete(f'/api/posts/{post_id}')
        data = json.loads(response.data)
        
        assert 'message' in data
        assert 'deleted' in data['message'].lower()


# ============================================================================
# TESTES DE BUSCA DE POSTS
# ============================================================================

class TestSearchPosts:
    """Testes para buscar posts"""
    
    def test_search_posts_without_query_returns_400(self, client):
        """Testa se busca sem query retorna 400"""
        response = client.get('/api/posts/search')
        assert response.status_code == 400
    
    def test_search_posts_with_empty_query_returns_400(self, client):
        """Testa se busca com query vazia retorna 400"""
        response = client.get('/api/posts/search?q=')
        assert response.status_code == 400
    
    def test_search_posts_returns_matching_results(self, client):
        """Testa se a busca retorna posts correspondentes"""
        # Criar múltiplos posts
        posts = [
            {'title': 'Python Tutorial', 'content': 'Aprenda Python'},
            {'title': 'Flask Guide', 'content': 'Guia do Flask'},
            {'title': 'Python Advanced', 'content': 'Python avançado'}
        ]
        
        for post in posts:
            client.post('/api/posts',
                       data=json.dumps(post),
                       content_type='application/json')
        
        # Buscar posts com 'Python'
        response = client.get('/api/posts/search?q=Python')
        data = json.loads(response.data)
        
        assert len(data) == 2
        assert all('Python' in post['title'] for post in data)
    
    def test_search_posts_case_insensitive(self, client):
        """Testa se a busca é case-insensitive"""
        # Criar post
        post = {'title': 'Python Tutorial', 'content': 'Conteúdo'}
        client.post('/api/posts',
                   data=json.dumps(post),
                   content_type='application/json')
        
        # Buscar com diferentes casos
        response1 = client.get('/api/posts/search?q=python')
        response2 = client.get('/api/posts/search?q=PYTHON')
        response3 = client.get('/api/posts/search?q=Python')
        
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        data3 = json.loads(response3.data)
        
        assert len(data1) == len(data2) == len(data3) == 1
    
    def test_search_posts_no_results(self, client):
        """Testa busca sem resultados"""
        # Criar um post
        post = {'title': 'Python', 'content': 'Conteúdo'}
        client.post('/api/posts',
                   data=json.dumps(post),
                   content_type='application/json')
        
        # Buscar termo que não existe
        response = client.get('/api/posts/search?q=NonExistent')
        data = json.loads(response.data)
        
        assert data == []


# ============================================================================
# TESTES DE INTEGRAÇÃO
# ============================================================================

class TestIntegration:
    """Testes de integração com fluxo completo"""
    
    def test_full_post_lifecycle(self, client, sample_post):
        """Testa ciclo de vida completo de um post"""
        # 1. Criar post
        create_response = client.post('/api/posts',
                                     data=json.dumps(sample_post),
                                     content_type='application/json')
        assert create_response.status_code == 201
        post_id = json.loads(create_response.data)['id']
        
        # 2. Obter post
        get_response = client.get(f'/api/posts/{post_id}')
        assert get_response.status_code == 200
        
        # 3. Atualizar post
        update_data = {'title': 'Título Atualizado'}
        update_response = client.put(f'/api/posts/{post_id}',
                                    data=json.dumps(update_data),
                                    content_type='application/json')
        assert update_response.status_code == 200
        
        # 4. Verificar atualização
        verify_response = client.get(f'/api/posts/{post_id}')
        updated_post = json.loads(verify_response.data)
        assert updated_post['title'] == 'Título Atualizado'
        
        # 5. Deletar post
        delete_response = client.delete(f'/api/posts/{post_id}')
        assert delete_response.status_code == 200
        
        # 6. Verificar deleção
        final_response = client.get(f'/api/posts/{post_id}')
        assert final_response.status_code == 404
    
    def test_multiple_posts_workflow(self, client, multiple_posts):
        """Testa fluxo com múltiplos posts"""
        # Criar múltiplos posts
        post_ids = []
        for post in multiple_posts:
            response = client.post('/api/posts',
                                 data=json.dumps(post),
                                 content_type='application/json')
            post_ids.append(json.loads(response.data)['id'])
        
        # Listar todos
        list_response = client.get('/api/posts')
        all_posts = json.loads(list_response.data)
        assert len(all_posts) == len(multiple_posts)
        
        # Buscar específicos
        search_response = client.get('/api/posts/search?q=Flask')
        search_results = json.loads(search_response.data)
        assert len(search_results) == 1
        assert search_results[0]['title'] == 'Flask Tutorial'
        
        # Deletar todos
        for post_id in post_ids:
            response = client.delete(f'/api/posts/{post_id}')
            assert response.status_code == 200
        
        # Verificar lista vazia
        final_response = client.get('/api/posts')
        final_posts = json.loads(final_response.data)
        assert len(final_posts) == 0


# ============================================================================
# TESTES DE TIPOS E VALIDAÇÕES
# ============================================================================

class TestDataValidation:
    """Testes para validação de dados"""
    
    def test_post_id_is_integer(self, client, sample_post):
        """Testa se o ID é um inteiro"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        data = json.loads(response.data)
        assert isinstance(data['id'], int)
    
    def test_post_has_all_required_fields(self, client, sample_post):
        """Testa se o post tem todos os campos necessários"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        data = json.loads(response.data)
        
        required_fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        for field in required_fields:
            assert field in data, f"Campo '{field}' não encontrado"
    
    def test_timestamps_are_iso_format(self, client, sample_post):
        """Testa se timestamps estão em formato ISO"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post),
                             content_type='application/json')
        data = json.loads(response.data)
        
        # Verificar formato ISO (deve conter 'T')
        assert 'T' in data['created_at']
        assert 'T' in data['updated_at']


# ============================================================================
# TESTES DE ERROS E EDGE CASES
# ============================================================================

class TestErrorHandling:
    """Testes para tratamento de erros"""
    
    def test_invalid_route_returns_404(self, client):
        """Testa se rota inválida retorna 404"""
        response = client.get('/api/invalid')
        assert response.status_code == 404
    
    def test_invalid_method_returns_error(self, client):
        """Testa se método inválido retorna erro"""
        response = client.patch('/api/posts/1')
        assert response.status_code != 200
    
    def test_malformed_json_returns_400(self, client):
        """Testa se JSON malformado retorna 400"""
        response = client.post('/api/posts',
                             data='{invalid json}',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_missing_content_type_with_json_data(self, client, sample_post):
        """Testa comportamento sem content-type apropriado"""
        response = client.post('/api/posts',
                             data=json.dumps(sample_post))
        # Pode ser 400 ou 415, dependendo da configuração
        assert response.status_code in [400, 415]


if __name__ == '__main__':
    # Para rodar os testes localmente
    pytest.main([__file__, '-v', '--tb=short'])