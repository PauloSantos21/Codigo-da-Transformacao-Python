import hashlib
from datetime import datetime, timedelta
from typing import Optional


# ============================================================================
# EXCEÇÕES PERSONALIZADAS
# ============================================================================

class CredenciaisInvalidasError(Exception):
    """Exceção levantada quando usuário ou senha está incorreto."""
    
    def __init__(self, tentativas_restantes: int):
        self.tentativas_restantes = tentativas_restantes
        mensagem = (
            f"Credenciais inválidas! "
            f"Tentativas restantes: {tentativas_restantes}"
        )
        super().__init__(mensagem)


class ContaBloqueadaError(Exception):
    """Exceção levantada quando conta é bloqueada por tentativas excessivas."""
    
    def __init__(self, tempo_desbloqueio: int):
        self.tempo_desbloqueio = tempo_desbloqueio
        mensagem = (
            f"Conta bloqueada por segurança! "
            f"Tente novamente em {tempo_desbloqueio} minuto(s)."
        )
        super().__init__(mensagem)


class UsuarioNaoEncontradoError(Exception):
    """Exceção levantada quando usuário não existe."""
    
    def __init__(self, usuario: str):
        self.usuario = usuario
        mensagem = f"Usuário '{usuario}' não encontrado no sistema."
        super().__init__(mensagem)


class SenhaFracaError(Exception):
    """Exceção levantada quando senha não atende requisitos de segurança."""
    
    def __init__(self, requisitos: list):
        self.requisitos = requisitos
        mensagem = f"Senha não atende aos requisitos: {', '.join(requisitos)}"
        super().__init__(mensagem)


# ============================================================================
# CLASSE USUÁRIO
# ============================================================================

class Usuario:
    """Classe que representa um usuário no sistema."""
    
    def __init__(self, usuario: str, senha: str, email: str = None):
        """
        Inicializa um usuário.
        
        Args:
            usuario (str): Nome de usuário
            senha (str): Senha (será hasheada)
            email (str): Email (opcional)
        """
        self.usuario = usuario
        self.senha_hash = self._hashear_senha(senha)
        self.email = email
        self.ativo = True
        self.bloqueado = False
        self.data_bloqueio = None
        self.tentativas_falhas = 0
        self.data_ultimo_acesso = None
        self.data_criacao = datetime.now()
    
    def _hashear_senha(self, senha: str) -> str:
        """Hasheia uma senha usando SHA-256."""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha fornecida está correta."""
        return self.senha_hash == self._hashear_senha(senha)
    
    def bloquear(self, minutos: int = 15):
        """Bloqueia a conta temporariamente."""
        self.bloqueado = True
        self.data_bloqueio = datetime.now()
        self.tempo_desbloqueio = minutos
    
    def desbloquear(self):
        """Desbloqueia a conta."""
        self.bloqueado = False
        self.data_bloqueio = None
        self.tentativas_falhas = 0
    
    def verificar_bloqueio(self) -> bool:
        """Verifica se a conta ainda está bloqueada."""
        if not self.bloqueado:
            return False
        
        tempo_decorrido = datetime.now() - self.data_bloqueio
        tempo_bloqueio = timedelta(minutes=self.tempo_desbloqueio)
        
        if tempo_decorrido >= tempo_bloqueio:
            self.desbloquear()
            return False
        
        return True
    
    def registrar_tentativa_falha(self):
        """Registra uma tentativa de login falhada."""
        self.tentativas_falhas += 1
    
    def registrar_acesso_bem_sucedido(self):
        """Registra um acesso bem-sucedido."""
        self.tentativas_falhas = 0
        self.data_ultimo_acesso = datetime.now()


# ============================================================================
# SISTEMA DE LOGIN
# ============================================================================

class SistemaLogin:
    """Sistema de login com autenticação e controle de segurança."""
    
    MAX_TENTATIVAS = 3
    TEMPO_BLOQUEIO = 15  # minutos
    
    def __init__(self):
        """Inicializa o sistema de login."""
        self.usuarios = {}
        self.usuario_logado = None
        self._criar_usuarios_padrao()
    
    def _criar_usuarios_padrao(self):
        """Cria alguns usuários padrão para teste."""
        self.registrar_usuario("admin", "Admin@123", "admin@email.com")
        self.registrar_usuario("joao", "Joao@456", "joao@email.com")
        self.registrar_usuario("maria", "Maria@789", "maria@email.com")
    
    def _validar_requisitos_senha(self, senha: str) -> list:
        """
        Valida requisitos de segurança da senha.
        
        Requisitos:
        - Mínimo 8 caracteres
        - Pelo menos uma letra maiúscula
        - Pelo menos uma letra minúscula
        - Pelo menos um número
        - Pelo menos um caractere especial
        
        Returns:
            list: Lista de requisitos não atendidos
        """
        requisitos_nao_atendidos = []
        
        if len(senha) < 8:
            requisitos_nao_atendidos.append("Mínimo 8 caracteres")
        if not any(c.isupper() for c in senha):
            requisitos_nao_atendidos.append("Letra maiúscula")
        if not any(c.islower() for c in senha):
            requisitos_nao_atendidos.append("Letra minúscula")
        if not any(c.isdigit() for c in senha):
            requisitos_nao_atendidos.append("Um número")
        if not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in senha):
            requisitos_nao_atendidos.append("Caractere especial")
        
        return requisitos_nao_atendidos
    
    def registrar_usuario(self, usuario: str, senha: str, email: str = None) -> bool:
        """
        Registra um novo usuário no sistema.
        
        Args:
            usuario (str): Nome de usuário
            senha (str): Senha
            email (str): Email (opcional)
        
        Returns:
            bool: True se registrado, False caso contrário
        """
        try:
            # Validar requisitos
            requisitos_invalidos = self._validar_requisitos_senha(senha)
            if requisitos_invalidos:
                raise SenhaFracaError(requisitos_invalidos)
            
            # Validar se usuário já existe
            if usuario in self.usuarios:
                print(f"❌ Erro: Usuário '{usuario}' já existe!")
                return False
            
            # Validar nome de usuário
            if not usuario or len(usuario) < 3:
                print("❌ Erro: Nome de usuário deve ter pelo menos 3 caracteres")
                return False
            
            # Registrar usuário
            self.usuarios[usuario] = Usuario(usuario, senha, email)
            print(f"✓ Usuário '{usuario}' registrado com sucesso!\n")
            return True
        
        except SenhaFracaError as erro:
            print(f"❌ Erro: {erro}\n")
            return False
        except Exception as erro:
            print(f"❌ Erro inesperado: {erro}\n")
            return False
    
    def fazer_login(self, usuario: str, senha: str) -> bool:
        """
        Realiza login no sistema.
        
        Args:
            usuario (str): Nome de usuário
            senha (str): Senha
        
        Returns:
            bool: True se login bem-sucedido
        
        Raises:
            UsuarioNaoEncontradoError: Se usuário não existe
            ContaBloqueadaError: Se conta está bloqueada
            CredenciaisInvalidasError: Se senha está incorreta
        """
        try:
            # Verificar se usuário existe
            if usuario not in self.usuarios:
                raise UsuarioNaoEncontradoError(usuario)
            
            user = self.usuarios[usuario]
            
            # Verificar se conta está ativa
            if not user.ativo:
                print("❌ Erro: Conta desativada. Contate o administrador.\n")
                return False
            
            # Verificar se conta está bloqueada
            if user.verificar_bloqueio():
                tempo_restante = (
                    user.data_bloqueio + 
                    timedelta(minutes=user.tempo_desbloqueio) - 
                    datetime.now()
                ).seconds // 60
                raise ContaBloqueadaError(tempo_restante + 1)
            
            # Verificar senha
            if not user.verificar_senha(senha):
                user.registrar_tentativa_falha()
                
                # Bloquear se atingir limite de tentativas
                if user.tentativas_falhas >= self.MAX_TENTATIVAS:
                    user.bloquear(self.TEMPO_BLOQUEIO)
                    raise ContaBloqueadaError(self.TEMPO_BLOQUEIO)
                
                tentativas_restantes = self.MAX_TENTATIVAS - user.tentativas_falhas
                raise CredenciaisInvalidasError(tentativas_restantes)
            
            # Login bem-sucedido
            user.registrar_acesso_bem_sucedido()
            self.usuario_logado = usuario
            print(f"✓ Login bem-sucedido! Bem-vindo, {usuario}!\n")
            return True
        
        except UsuarioNaoEncontradoError as erro:
            print(f"❌ Erro: {erro}\n")
            return False
        except ContaBloqueadaError as erro:
            print(f"❌ Erro: {erro}\n")
            return False
        except CredenciaisInvalidasError as erro:
            print(f"❌ Erro: {erro}\n")
            return False
        except Exception as erro:
            print(f"❌ Erro inesperado: {erro}\n")
            return False
    
    def fazer_logout(self) -> bool:
        """Faz logout do sistema."""
        if self.usuario_logado is None:
            print("❌ Erro: Nenhum usuário logado.\n")
            return False
        
        usuario = self.usuario_logado
        self.usuario_logado = None
        print(f"✓ Logout realizado. Até logo, {usuario}!\n")
        return True
    
    def verificar_usuario_logado(self) -> Optional[str]:
        """Retorna o usuário atualmente logado."""
        return self.usuario_logado
    
    def listar_usuarios(self) -> None:
        """Lista todos os usuários registrados."""
        print("\n" + "=" * 60)
        print("USUÁRIOS DO SISTEMA")
        print("=" * 60)
        
        if not self.usuarios:
            print("Nenhum usuário registrado.\n")
            return
        
        for nome, user in self.usuarios.items():
            status = "Ativo" if user.ativo else "Inativo"
            bloqueio = "Bloqueado" if user.bloqueado else "Desbloqueado"
            ultimo_acesso = (
                user.data_ultimo_acesso.strftime("%d/%m/%Y %H:%M:%S")
                if user.data_ultimo_acesso
                else "Nunca acessou"
            )
            
            print(f"\nUsuário: {nome}")
            print(f"  Email: {user.email or 'Não informado'}")
            print(f"  Status: {status}")
            print(f"  Bloqueio: {bloqueio}")
            print(f"  Último acesso: {ultimo_acesso}")
            print(f"  Data de criação: {user.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}")
        
        print("=" * 60 + "\n")


# ============================================================================
# INTERFACE INTERATIVA
# ============================================================================

def menu_principal():
    """Menu principal do sistema."""
    sistema = SistemaLogin()
    
    while True:
        print("\n" + "=" * 60)
        print(" SISTEMA DE LOGIN")
        print("=" * 60)
        
        if sistema.verificar_usuario_logado():
            usuario = sistema.verificar_usuario_logado()
            print(f"\n[Logado como: {usuario}]")
            print("\n1. Fazer logout")
            print("2. Ver informações do usuário")
            print("3. Listar todos os usuários")
            print("4. Sair")
        else:
            print("\n1. Fazer login")
            print("2. Registrar novo usuário")
            print("3. Listar usuários")
            print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        try:
            if not sistema.verificar_usuario_logado():
                if opcao == "1":
                    usuario = input("Usuário: ").strip()
                    senha = input("Senha: ").strip()
                    sistema.fazer_login(usuario, senha)
                
                elif opcao == "2":
                    usuario = input("Novo usuário: ").strip()
                    email = input("Email (opcional): ").strip() or None
                    senha = input("Senha: ").strip()
                    sistema.registrar_usuario(usuario, senha, email)
                
                elif opcao == "3":
                    sistema.listar_usuarios()
                
                elif opcao == "4":
                    print("Encerrando sistema...")
                    break
                
                else:
                    print("❌ Opção inválida!")
            else:
                if opcao == "1":
                    sistema.fazer_logout()
                
                elif opcao == "2":
                    user = sistema.usuarios[sistema.verificar_usuario_logado()]
                    print(f"\nInformações do usuário:")
                    print(f"  Usuário: {user.usuario}")
                    print(f"  Email: {user.email or 'Não informado'}")
                    print(f"  Último acesso: {user.data_ultimo_acesso.strftime('%d/%m/%Y %H:%M:%S')}")
                
                elif opcao == "3":
                    sistema.listar_usuarios()
                
                elif opcao == "4":
                    sistema.fazer_logout()
                    print("Encerrando sistema...")
                    break
                
                else:
                    print("❌ Opção inválida!")
        
        except KeyboardInterrupt:
            print("\n\nSistema interrompido pelo usuário.")
            break
        except Exception as erro:
            print(f"❌ Erro: {erro}")


# ============================================================================
# EXEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" EXEMPLOS: SISTEMA DE LOGIN COM TRATAMENTO DE ERROS")
    print("=" * 60 + "\n")
    
    sistema = SistemaLogin()
    
    # Exemplo 1: Login bem-sucedido
    print("--- Exemplo 1: Login Bem-sucedido ---")
    sistema.fazer_login("admin", "Admin@123")
    sistema.fazer_logout()
    
    # Exemplo 2: Usuário não encontrado
    print("--- Exemplo 2: Usuário Não Encontrado ---")
    sistema.fazer_login("usuario_inexistente", "qualquer_senha")
    
    # Exemplo 3: Senha incorreta
    print("--- Exemplo 3: Senha Incorreta ---")
    sistema.fazer_login("joao", "senha_errada")
    
    # Exemplo 4: Múltiplas tentativas (conta bloqueada)
    print("--- Exemplo 4: Múltiplas Tentativas Falhas ---")
    sistema.fazer_login("maria", "errada1")
    sistema.fazer_login("maria", "errada2")
    sistema.fazer_login("maria", "errada3")  # Vai bloquear
    
    # Exemplo 5: Registrar novo usuário com senha fraca
    print("--- Exemplo 5: Registrar Usuário com Senha Fraca ---")
    sistema.registrar_usuario("carlos", "123", "carlos@email.com")
    
    # Exemplo 6: Registrar novo usuário com sucesso
    print("--- Exemplo 6: Registrar Usuário com Sucesso ---")
    sistema.registrar_usuario("pedro", "Pedro@2025!", "pedro@email.com")
    sistema.fazer_login("pedro", "Pedro@2025!")
    
    # Menu interativo
    print("\n" + "=" * 60)
    print(" MENU INTERATIVO")
    print("=" * 60)
    resposta = input("\nDeseja usar o menu interativo? (s/n): ").strip().lower()
    if resposta == "s":
        menu_principal()