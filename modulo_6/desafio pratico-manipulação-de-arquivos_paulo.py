import json
import csv
import os
import shutil

# =================================================================
## 1. 📄 Atividade 1: Criar, Gravar e Ler um Arquivo .txt
# =================================================================

def atividade_1_txt():
    """Cria, escreve e lê um arquivo de texto simples."""
    print("="*60)
    print("## 1. Atividade: Manipulação de Arquivo TXT")
    print("="*60)
    
    nome_arquivo_txt = "dados.txt"
    conteudo_a_escrever = (
        "Linha 1: Olá, este é o teste de gravação!\n"
        "Linha 2: Este é um arquivo de texto simples.\n"
        "Linha 3: Atividade 1 concluída com sucesso.\n"
    )

    try:
        # ESCREVER (write) no arquivo
        with open(nome_arquivo_txt, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo_a_escrever)
        print(f"✅ Sucesso! Dados gravados em '{nome_arquivo_txt}'.")

        # LER (read) o arquivo
        with open(nome_arquivo_txt, 'r', encoding='utf-8') as arquivo:
            conteudo_lido = arquivo.read()
        
        print(f"\nConteúdo lido de '{nome_arquivo_txt}':")
        print("-" * 30)
        print(conteudo_lido.strip())
        print("-" * 30)

    except IOError as e:
        print(f"❌ Erro ao manipular o arquivo TXT: {e}")

# ---

# =================================================================
## 2. 💾 Atividade 2: Salvar e Carregar um Dicionário em JSON
# =================================================================

def atividade_2_json():
    """Salva um dicionário de clientes em JSON e o carrega."""
    print("\n\n" + "="*60)
    print("## 2. Atividade: Manipulação de Arquivo JSON")
    print("="*60)
    
    nome_arquivo_json = "clientes.json"

    dados_clientes = {
        "cliente_001": {"nome": "Maria Silva", "cidade": "São Paulo", "saldo": 1250.75},
        "cliente_002": {"nome": "João Santos", "cidade": "Rio de Janeiro", "saldo": 500.00},
        "cliente_003": {"nome": "Ana Souza", "cidade": "Belo Horizonte", "saldo": 3400.90}
    }

    try:
        # SALVAR (dump) no arquivo JSON
        with open(nome_arquivo_json, 'w', encoding='utf-8') as arquivo:
            # indent=4 para melhor legibilidade
            json.dump(dados_clientes, arquivo, indent=4)
        print(f"✅ Sucesso! Dicionário de clientes salvo em '{nome_arquivo_json}'.")

        # CARREGAR (load) do arquivo JSON
        with open(nome_arquivo_json, 'r', encoding='utf-8') as arquivo:
            dados_carregados = json.load(arquivo)
        
        print("\nDados de Clientes Carregados (formato Python Dicionário):")
        print(dados_carregados)
        
        # Exemplo de acesso:
        nome_cliente = dados_carregados['cliente_001']['nome']
        print(f"\nDetalhe Carregado: O primeiro cliente é {nome_cliente}.")

    except (IOError, json.JSONDecodeError) as e:
        print(f"❌ Erro ao manipular o arquivo JSON: {e}")

# ---

# =================================================================
## 3. 📈 Atividade 3: Sistema de Notas com Arquivo CSV
# =================================================================

def atividade_3_csv():
    """Adiciona notas e exibe o conteúdo de um arquivo CSV."""
    print("\n\n" + "="*60)
    print("## 3. Atividade: Sistema de Notas com CSV")
    print("="*60)
    
    nome_arquivo_csv = "notas_alunos.csv"
    cabecalho = ["Nome", "Materia", "Nota"]
    
    def adicionar_nota(nome, materia, nota):
        """Adiciona uma nova linha (registro) ao arquivo CSV."""
        try:
            # 'a' (append) para anexar, 'newline=''' para evitar linhas em branco
            arquivo_existe = os.path.exists(nome_arquivo_csv)
            escrever_cabecalho = not arquivo_existe or os.path.getsize(nome_arquivo_csv) == 0

            with open(nome_arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo:
                escritor_csv = csv.writer(arquivo)
                
                if escrever_cabecalho:
                    escritor_csv.writerow(cabecalho)
                    
                escritor_csv.writerow([nome, materia, nota])
                print(f"  > Nota de {nome} em {materia} adicionada.")
                
        except IOError as e:
            print(f"❌ Erro ao escrever no arquivo CSV: {e}")

    def carregar_e_exibir_notas():
        """Carrega e exibe o conteúdo do arquivo CSV de forma formatada."""
        print(f"\nConteúdo do arquivo CSV '{nome_arquivo_csv}':")
        if not os.path.exists(nome_arquivo_csv):
            print("  O arquivo CSV não existe. Adicione notas primeiro.")
            return

        try:
            with open(nome_arquivo_csv, 'r', newline='', encoding='utf-8') as arquivo:
                leitor_csv = csv.reader(arquivo)
                
                # Exibição formatada
                print(f"{cabecalho[0]:<15} | {cabecalho[1]:<10} | {cabecalho[2]:>5}")
                print("-" * 35)
                
                # Pula o cabeçalho para leitura formatada dos dados
                next(leitor_csv) 
                for nome, materia, nota in leitor_csv:
                    print(f"{nome:<15} | {materia:<10} | {nota:>5}")
            
            print("\n✅ Leitura do CSV concluída.")

        except (IOError, StopIteration) as e:
            print(f"❌ Erro ao ler o arquivo CSV: {e}")

    # --- Execução da Atividade 3 ---
    print("Adicionando dados de exemplo...")
    adicionar_nota("Carlos", "Matemática", 8.5)
    adicionar_nota("Fernanda", "História", 9.2)
    adicionar_nota("Carlos", "Português", 7.0)

    # Carregar e exibir as notas
    carregar_e_exibir_notas()

# --- 4. Desafio Extra: Sistema de Backup Automático com shutil


def desafio_extra_backup():
    """Cria pastas, arquivos de teste e realiza uma cópia de backup."""
    print("\n\n" + "="*60)
    print("## 4. Desafio Extra: Backup com shutil")
    print("="*60)
    
    PASTA_ORIGEM = "dados_origem"
    PASTA_DESTINO = "backup_destino"

    def preparar_ambiente():
        """Cria a estrutura de pastas e alguns arquivos para teste."""
        os.makedirs(PASTA_ORIGEM, exist_ok=True)
        os.makedirs(PASTA_DESTINO, exist_ok=True)
        
        # Cria arquivos fictícios na pasta de origem
        with open(os.path.join(PASTA_ORIGEM, "documento_a.txt"), 'w') as f:
            f.write("Conteúdo importante do Documento A.")
        with open(os.path.join(PASTA_ORIGEM, "relatorio_b.pdf"), 'w') as f:
            f.write("Simulando um PDF.") 
        
        print(f"✅ Ambiente preparado: '{PASTA_ORIGEM}' e '{PASTA_DESTINO}' criadas.")

    def realizar_backup():
        """Copia todos os arquivos da PASTA_ORIGEM para a PASTA_DESTINO."""
        print("\nIniciando Backup...")
        
        try:
            # Itera sobre todos os itens na pasta de origem
            arquivos_copiados = 0
            for item in os.listdir(PASTA_ORIGEM):
                caminho_origem = os.path.join(PASTA_ORIGEM, item)
                caminho_destino = os.path.join(PASTA_DESTINO, item)

                if os.path.isfile(caminho_origem):
                    # shutil.copy() copia o arquivo
                    shutil.copy(caminho_origem, caminho_destino)
                    print(f"  > Copiado: {item}")
                    arquivos_copiados += 1
            
            print(f"\n✅ Backup concluído! Total de {arquivos_copiados} arquivos copiados.")
            
            # Opcional: Verifica os arquivos na pasta de destino
            print(f"Arquivos na pasta de backup: {os.listdir(PASTA_DESTINO)}")
            
        except (shutil.Error, OSError) as e:
            print(f"❌ Erro durante a cópia ou sistema operacional: {e}")

    # --- Execução do Desafio Extra ---
    preparar_ambiente()
    realizar_backup()

## Execução Principal do Script
if __name__ == "__main__":
    atividade_1_txt()
    atividade_2_json()
    atividade_3_csv()
    desafio_extra_backup()
    
    print("\n\n" + "="*60)
    print("FIM DE TODAS AS ATIVIDADES. Verifique o seu diretório!")
    print("Os arquivos (dados.txt, clientes.json, notas_alunos.csv) e")
    print("as pastas (dados_origem, backup_destino) foram criados.")
    print("="*60)