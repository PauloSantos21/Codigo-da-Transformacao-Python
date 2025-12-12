"""
Guia Completo de Testes Automatizados com pytest e Flask

INSTALAÇÃO DAS DEPENDÊNCIAS
============================
Execute os seguintes comandos no terminal:

pip install pytest pytest-cov pytest-flask pytest-mock flask

ESTRUTURA DO PROJETO
====================
modulo_12/
├── implemente_testes_teste_automatizados.py  (Suite de testes)
│
modulo_13/
├── crie_api_para_blog.py                     (API Flask)
├── config_servidor_dev_api_com_flask.py      (Configurações)


EXECUTANDO OS TESTES
====================

1. Testes Básicos:
   pytest implemente_testes_teste_automatizados.py

2. Testes com Saída Detalhada:
   pytest implemente_testes_teste_automatizados.py -v

3. Testes com Prints Visíveis:
   pytest implemente_testes_teste_automatizados.py -v -s

4. Testes com Cobertura de Código:
   pytest implemente_testes_teste_automatizados.py --cov

5. Rodar Teste Específico:
   pytest implemente_testes_teste_automatizados.py::TestCreatePost::test_create_post_returns_201 -v

6. Rodar Classe Específica:
   pytest implemente_testes_teste_automatizados.py::TestCreatePost -v

7. Testes com Parada no Primeiro Erro:
   pytest implemente_testes_teste_automatizados.py -x

8. Testes com Histórico de Últimos Falhos:
   pytest implemente_testes_teste_automatizados.py --lf

9. Relatório Detalhado:
   pytest implemente_testes_teste_automatizados.py --tb=long -v


CONCEITOS PRINCIPAIS
====================

1. FIXTURES
   --------
   Fixtures são funções que fornecem dados ou configurações para os testes.
   
   @pytest.fixture
   def client(app):
       return app.test_client()
   
   def test_something(client):  # client é injetado automaticamente
       response = client.get('/api/health')


2. CLASSES DE TESTE
   ----------------
   Organizam testes relacionados e facilitam manutenção:
   
   class TestCreatePost:
       def test_create_post_returns_201(self, client):
           ...
       
       def test_create_post_returns_post_data(self, client):
           ...


3. ARRANCAR, AGIR, AFIRMAR (AAA)
   ----------------------------
   Padrão para estruturar testes:
   
   def test_something(client, sample_post):
       # ARRANCAR: Preparar dados
       response = client.post('/api/posts', data=json.dumps(sample_post), ...)
       
       # AGIR: Executar ação
       post_id = json.loads(response.data)['id']
       
       # AFIRMAR: Verificar resultado
       assert response.status_code == 201
       assert post_id is not None


4. ASSERÇÕES
   ----------
   assert condition                      # Verificação simples
   assert response.status_code == 200    # Comparação
   assert len(data) == 3                 # Tamanho
   assert 'title' in data                # Pertencimento
   assert data['id'] != expected_id      # Desigualdade


5. PARAMETRIZAÇÃO
   ---------------
   Para rodar o mesmo teste com diferentes valores:
   
   @pytest.mark.parametrize("status_code,message", [
       (200, "Success"),
       (404, "Not found"),
       (500, "Error")
   ])
   def test_status_codes(client, status_code, message):
       ...


6. MOCKING
   -------
   Para mockar dependências externas:
   
   from unittest.mock import patch, MagicMock
   
   @patch('modulo_13.crie_api_para_blog.datetime')
   def test_with_mock(mock_datetime, client):
       mock_datetime.now.return_value = ...
       ...


ESTRUTURA DE TESTES NA SUÍTE
============================

✓ TestHealthCheck
  - test_health_endpoint_returns_200
  - test_health_endpoint_returns_healthy_status
  - test_health_endpoint_includes_timestamp

✓ TestListPosts
  - test_list_posts_returns_200
  - test_list_posts_returns_empty_list_initially
  - test_list_posts_returns_json
  - test_list_posts_after_creation

✓ TestCreatePost
  - test_create_post_returns_201
  - test_create_post_returns_post_data
  - test_create_post_assigns_id
  - test_create_post_includes_timestamps
  - test_create_post_without_title_returns_400
  - test_create_post_without_content_returns_400
  - test_create_post_with_empty_title_returns_400
  - test_create_post_without_json_returns_400
  - test_create_post_with_default_author

✓ TestGetPost
  - test_get_existing_post_returns_200
  - test_get_nonexistent_post_returns_404
  - test_get_post_returns_correct_data
  - test_get_post_error_message

✓ TestUpdatePost
  - test_update_post_returns_200
  - test_update_nonexistent_post_returns_404
  - test_update_post_title
  - test_update_post_content
  - test_update_post_multiple_fields
  - test_update_post_updates_timestamp

✓ TestDeletePost
  - test_delete_post_returns_200
  - test_delete_nonexistent_post_returns_404
  - test_delete_post_removes_from_list
  - test_delete_post_success_message

✓ TestSearchPosts
  - test_search_posts_without_query_returns_400
  - test_search_posts_with_empty_query_returns_400
  - test_search_posts_returns_matching_results
  - test_search_posts_case_insensitive
  - test_search_posts_no_results

✓ TestIntegration
  - test_full_post_lifecycle
  - test_multiple_posts_workflow

✓ TestDataValidation
  - test_post_id_is_integer
  - test_post_has_all_required_fields
  - test_timestamps_are_iso_format

✓ TestErrorHandling
  - test_invalid_route_returns_404
  - test_invalid_method_returns_error
  - test_malformed_json_returns_400
  - test_missing_content_type_with_json_data


BOAS PRÁTICAS
==============

1. Nomes Descritivos
   - Use nomes que descrevem o que está sendo testado
   - test_create_post_returns_201 (bom)
   - test_post (ruim)

2. Um Comportamento por Teste
   - Cada teste deve verificar um único comportamento
   - Evite testes que fazem múltiplas coisas

3. Arrange-Act-Assert
   - Organize os testes nessa estrutura
   - Fica mais claro o fluxo

4. DRY (Don't Repeat Yourself)
   - Use fixtures para evitar duplicação
   - Reutilize código comum

5. Testes Independentes
   - Testes não devem depender um do outro
   - Use setup e teardown quando necessário

6. Cobertura Adequada
   - Aim para 80%+ de cobertura de código
   - Foque em fluxos críticos primeiro

7. Nomes de Fixtures Claros
   - @pytest.fixture def sample_post() ✓
   - @pytest.fixture def data() ✗


LEITURA RECOMENDADA
===================

1. Documentação oficial pytest:
   https://docs.pytest.org/

2. Documentação Flask Testing:
   https://flask.palletsprojects.com/testing/

3. Best Practices for Testing:
   https://en.wikipedia.org/wiki/Test-driven_development


PRÓXIMOS PASSOS
==============

1. Execute os testes:
   pytest implemente_testes_teste_automatizados.py -v

2. Examine a cobertura:
   pytest implemente_testes_teste_automatizados.py --cov

3. Adicione novos testes conforme necessário

4. Integre com CI/CD (GitHub Actions, GitLab CI, etc)

5. Configure pre-commit hooks para rodar testes automaticamente
"""

# Exemplos de extensão dos testes

# EXEMPLO 1: Parametrização
"""
@pytest.mark.parametrize("title,content,author", [
    ("Post 1", "Conteúdo 1", "Autor 1"),
    ("Post 2", "Conteúdo 2", "Autor 2"),
    ("Post 3", "Conteúdo 3", "Autor 3"),
])
def test_create_multiple_posts(client, title, content, author):
    post = {'title': title, 'content': content, 'author': author}
    response = client.post('/api/posts',
                         data=json.dumps(post),
                         content_type='application/json')
    assert response.status_code == 201
"""

# EXEMPLO 2: Mocking
"""
from unittest.mock import patch, MagicMock

@patch('datetime.datetime')
def test_timestamp_mock(mock_datetime, client, sample_post):
    # Mocka o datetime
    mock_now = MagicMock()
    mock_datetime.now.return_value = mock_now
    
    response = client.post('/api/posts',
                         data=json.dumps(sample_post),
                         content_type='application/json')
    data = json.loads(response.data)
    
    # Verifica que o mock foi chamado
    assert mock_datetime.now.called
"""

# EXEMPLO 3: Fixtures com escopos
"""
@pytest.fixture(scope="session")  # Executado uma vez por sessão
def app():
    app = create_app()
    app.config.from_object(TestingConfig)
    return app

@pytest.fixture(scope="function")  # Executado para cada teste
def client(app):
    return app.test_client()
"""

# EXEMPLO 4: Setup e Teardown
"""
class TestDatabase:
    def setup_method(self):
        # Executado antes de cada teste
        self.db = Database()
        self.db.connect()
    
    def teardown_method(self):
        # Executado após cada teste
        self.db.disconnect()
    
    def test_query(self):
        result = self.db.query("SELECT * FROM posts")
        assert result is not None
"""

# EXEMPLO 5: Fixtures com finalizers
"""
@pytest.fixture
def database():
    db = Database()
    db.connect()
    
    # Cleanup
    yield db
    
    db.disconnect()

def test_with_database(database):
    result = database.query("SELECT * FROM posts")
    assert result is not None
"""