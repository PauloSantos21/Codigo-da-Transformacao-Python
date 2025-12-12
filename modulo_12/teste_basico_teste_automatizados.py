"""
Testes Básicos - Para Iniciantes em pytest

Este arquivo contém exemplos simples e didáticos de testes
com pytest, focado em conceitos fundamentais.

Módulo: Testes Automatizados
"""

import pytest
import json
import sys
from pathlib import Path

# Importar a API
sys.path.insert(0, str(Path(__file__).parent.parent / 'modulo_13'))
from modulo_13.crie_api_para_blog_dev_api_com_flask import create_app
from config_servidor_dev_api_com_flask import TestingConfig


# ============================================================================
# PARTE 1: O QUE É UMA FIXTURE?
# ============================================================================

"""
Fixture é uma função que prepara dados para seus testes.

Sem fixture (ruim):
    def test_1():
        app = create_app()
        client = app.test_client()
        # usa client
    
    def test_2():
        app = create_app()
        client = app.test_client()
        # usa client (código duplicado!)

Com fixture (bom):
    @pytest.fixture
    def client(app):
        return app.test_client()
    
    def test_1(client):
        # usa client
    
    def test_2(client):
        # usa client (sem duplicação!)
"""

@pytest.fixture
def app():
    """Cria a aplicação Flask para testes"""
    app = create_app()
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Cria um cliente de teste baseado na app"""
    return app.test_client()


@pytest.fixture
def novo_post():
    """Dados de um post novo"""
    return {
        'title': 'Aprender pytest',
        'content': 'pytest é incrível!',
        'author': 'João'
    }


# ============================================================================
# PARTE 2: TESTES SIMPLES (básico)
# ============================================================================

class TestO1_Basic:
    """Testes básicos - começamos aqui"""
    
    def test_api_responde(self, client):
        """
        Teste mais simples possível:
        Verifica se a API responde
        """
        response = client.get('/api/health')
        
        # O que significa?
        # response = resultado da requisição GET
        # status_code = código HTTP (200 = OK, 404 = Not found, etc)
        assert response.status_code == 200
    
    def test_saude_da_api(self, client):
        """Verifica se a API está saudável"""
        response = client.get('/api/health')
        
        # Convertendo JSON para dicionário Python
        dados = json.loads(response.data)
        
        # Verificando se o status é 'healthy'
        assert dados['status'] == 'healthy'
    
    def test_lista_vazia_inicialmente(self, client):
        """Posts devem estar vazios no início"""
        response = client.get('/api/posts')
        dados = json.loads(response.data)
        
        # Uma lista vazia em JSON é []
        assert len(dados) == 0


# ============================================================================
# PARTE 3: TESTES COM DADOS (usando fixtures)
# ============================================================================

class TestO2_ComDados:
    """Testes usando dados fornecidos por fixtures"""
    
    def test_criar_post(self, client, novo_post):
        """
        Cria um post e verifica se foi criado
        
        Explicação:
        - client: vem da fixture client()
        - novo_post: vem da fixture novo_post()
        - pytest injeta automaticamente!
        """
        response = client.post(
            '/api/posts',
            data=json.dumps(novo_post),
            content_type='application/json'
        )
        
        # 201 = Created (post foi criado com sucesso)
        assert response.status_code == 201
    
    def test_post_criado_tem_id(self, client, novo_post):
        """Verifica se post criado recebe um ID"""
        response = client.post(
            '/api/posts',
            data=json.dumps(novo_post),
            content_type='application/json'
        )
        
        dados = json.loads(response.data)
        
        # O post deve ter um ID
        assert 'id' in dados
        assert dados['id'] > 0
    
    def test_post_criado_tem_todos_campos(self, client, novo_post):
        """Verifica se post tem todos os campos"""
        response = client.post(
            '/api/posts',
            data=json.dumps(novo_post),
            content_type='application/json'
        )
        
        dados = json.loads(response.data)
        
        # Campos esperados
        campos_obrigatorios = ['id', 'title', 'content', 'author']
        
        for campo in campos_obrigatorios:
            assert campo in dados, f"Campo '{campo}' faltando!"


# ============================================================================
# PARTE 4: FLUXO COMPLETO (CRUD)
# ============================================================================

class TestO3_FluxoCompleto:
    """Teste que cria, lê, atualiza e deleta um post"""
    
    def test_crud_completo(self, client, novo_post):
        """
        C = Create (criar)
        R = Read (ler)
        U = Update (atualizar)
        D = Delete (deletar)
        """
        
        # STEP 1: CREATE - Criar post
        print("\n1️⃣  Criando post...")
        response = client.post(
            '/api/posts',
            data=json.dumps(novo_post),
            content_type='application/json'
        )
        assert response.status_code == 201
        post_id = json.loads(response.data)['id']
        print(f"   ✅ Post criado com ID {post_id}")
        
        # STEP 2: READ - Ler post
        print("\n2️⃣  Lendo post...")
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 200
        post = json.loads(response.data)
        assert post['title'] == novo_post['title']
        print(f"   ✅ Post obtido: {post['title']}")
        
        # STEP 3: UPDATE - Atualizar post
        print("\n3️⃣  Atualizando post...")
        atualizacao = {'title': 'Novo Título'}
        response = client.put(
            f'/api/posts/{post_id}',
            data=json.dumps(atualizacao),
            content_type='application/json'
        )
        assert response.status_code == 200
        post_atualizado = json.loads(response.data)
        assert post_atualizado['title'] == 'Novo Título'
        print(f"   ✅ Post atualizado: {post_atualizado['title']}")
        
        # STEP 4: DELETE - Deletar post
        print("\n4️⃣  Deletando post...")
        response = client.delete(f'/api/posts/{post_id}')
        assert response.status_code == 200
        print(f"   ✅ Post deletado")
        
        # STEP 5: VERIFY - Verificar deleção
        print("\n5️⃣  Verificando deleção...")
        response = client.get(f'/api/posts/{post_id}')
        assert response.status_code == 404
        print(f"   ✅ Confirmado: Post não existe mais")


# ============================================================================
# PARTE 5: TESTANDO ERROS
# ============================================================================

class TestO4_Erros:
    """Testando o que acontece quando algo dá errado"""
    
    def test_criar_post_sem_titulo_falha(self, client):
        """Criar post sem título deve retornar erro 400"""
        post_invalido = {
            'content': 'Tem conteúdo mas não tem título'
        }
        
        response = client.post(
            '/api/posts',
            data=json.dumps(post_invalido),
            content_type='application/json'
        )
        
        # 400 = Bad Request (requisição inválida)
        assert response.status_code == 400
    
    def test_obter_post_inexistente_falha(self, client):
        """Tentar obter post que não existe deve retornar 404"""
        response = client.get('/api/posts/999')
        
        # 404 = Not Found (não encontrado)
        assert response.status_code == 404
    
    def test_mensagem_de_erro_clara(self, client):
        """Erro deve conter mensagem clara"""
        response = client.get('/api/posts/999')
        dados = json.loads(response.data)
        
        # Deve ter um campo 'error'
        assert 'error' in dados
        assert dados['error'] == 'Post not found'


# ============================================================================
# PARTE 6: ASSERÇÕES ÚTEIS
# ============================================================================

class TestO5_AssercoesUteis:
    """Exemplos de diferentes tipos de asserção"""
    
    def test_igualdade(self, client):
        """Testar se valores são iguais"""
        response = client.get('/api/health')
        dados = json.loads(response.data)
        
        # Igual
        assert dados['status'] == 'healthy'
        # Diferente
        assert dados['status'] != 'sick'
    
    def test_comparacoes(self, client, novo_post):
        """Testar comparações numéricas"""
        response = client.post(
            '/api/posts',
            data=json.dumps(novo_post),
            content_type='application/json'
        )
        dados = json.loads(response.data)
        
        # Maior/menor
        assert dados['id'] > 0
        assert dados['id'] >= 1
    
    def test_pertencimento(self, client):
        """Testar se elemento está em coleção"""
        response = client.get('/api/health')
        dados = json.loads(response.data)
        
        # Campo existe?
        assert 'status' in dados
        assert 'timestamp' in dados
        assert 'inexistente' not in dados
    
    def test_tipo(self, client):
        """Testar tipos de dados"""
        response = client.get('/api/posts')
        dados = json.loads(response.data)
        
        # Tipo
        assert isinstance(dados, list)
        assert isinstance(response.status_code, int)
    
    def test_verdadeiro_falso(self, client):
        """Testar valores booleanos"""
        response = client.get('/api/health')
        
        # Verdadeiro
        assert response.status_code == 200  # True
        assert response.content_type == 'application/json'  # True
        
        # Falso
        assert not (response.status_code == 404)  # False


# ============================================================================
# PARTE 7: PARAMETRIZAÇÃO (VERSÃO SIMPLES)
# ============================================================================

class TestO6_Parametrizacao:
    """Rodar o mesmo teste com diferentes valores"""
    
    @pytest.mark.parametrize("titulo,conteudo", [
        ("Python", "Linguagem Python"),
        ("Flask", "Framework Flask"),
        ("Testes", "Testes em Python"),
    ])
    def test_criar_multiplos_posts(self, client, titulo, conteudo):
        """Cria posts com diferentes dados"""
        novo_post = {
            'title': titulo,
            'content': conteudo,
            'author': 'Teste'
        }
        
        response = client.post(
            '/api/posts',
            data=json.dumps(novo_post),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        dados = json.loads(response.data)
        assert dados['title'] == titulo


# ============================================================================
# RESUMO E DICAS
# ============================================================================

"""
RESUMO DO QUE APRENDEMOS:
=========================

1. FIXTURE (@pytest.fixture)
   Prepara dados para testes

2. TESTE SIMPLES
   def test_algo(client):
       response = client.get('/api/...')
       assert response.status_code == 200

3. ARRANCAR-AGIR-AFIRMAR (AAA)
   # Arrancar: preparar dados
   # Agir: executar ação
   # Afirmar: verificar resultado

4. ASSERÇÕES
   assert x == y              # Igualdade
   assert x in lista          # Pertencimento
   assert isinstance(x, type) # Tipo
   assert x > 0               # Comparação

5. PARAMETRIZAÇÃO
   @pytest.mark.parametrize("param", [val1, val2])
   def test_algo(param):
       ...

6. ESTRUTURA DE TESTE
   class Test...
       def test_...
           # Seu teste aqui


DICAS IMPORTANTES:
==================

✅ Nomes descritivos:
   test_criar_post_sucesso ✓
   test_error ✗

✅ Um comportamento por teste:
   Não misture múltiplas coisas no mesmo teste

✅ Nomes de fixtures claros:
   @pytest.fixture def client ✓
   @pytest.fixture def x ✗

✅ Use AAA (Arrange-Act-Assert):
   Fica mais claro e fácil entender

✅ Teste casos de erro também:
   Não só o caminho feliz


PRÓXIMOS PASSOS:
================

1. Execute este arquivo:
   pytest modulo_12/teste_basico_teste_automatizados.py -v

2. Leia os testes e entenda cada linha

3. Modifique os testes para praticar

4. Estude implemente_testes_teste_automatizados.py para padrões mais complexos

5. Leia GUIA_TESTES_PYTEST.md para conceitos avançados


Parabéns! Você agora entende o básico de testes com pytest! 🎉
"""


if __name__ == '__main__':
    # Para rodar com outputs visíveis
    pytest.main([__file__, '-v', '-s'])