
from flask import Flask, request, jsonify, g
import sqlite3
import re
from werkzeug.security import generate_password_hash
from datetime import datetime
from typing import Optional

DB_PATH = "clientes.db"
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)

# -----------------------
# Utilitários do banco
# -----------------------
def get_conn() -> sqlite3.Connection:
    conn = getattr(g, "_database", None)
    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g._database = conn
    return conn

@app.teardown_appcontext
def close_conn(exception):
    conn = getattr(g, "_database", None)
    if conn is not None:
        conn.close()

def init_db():
    """Cria a tabela users se não existir."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()

# Inicializa DB ao importar/executar
init_db()

# -----------------------
# Rotas
# -----------------------
@app.route("/saudacao", methods=["GET"])
def saudacao():
    return jsonify({"mensagem": "Olá! Bem-vindo ao servidor Flask."})

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    """
    Espera JSON:
    {
      "nome": "Fulano",
      "email": "fulano@example.com",
      "senha": "minhaSenhaSegura"
    }
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400

    data = request.get_json()

    # Validações básicas
    nome: Optional[str] = data.get("nome")
    email: Optional[str] = data.get("email")
    senha: Optional[str] = data.get("senha")

    if not nome or not isinstance(nome, str) or len(nome.strip()) < 2:
        return jsonify({"erro": "Campo 'nome' inválido (mínimo 2 caracteres)."}), 400

    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email):
        return jsonify({"erro": "Campo 'email' inválido."}), 400

    if not senha or not isinstance(senha, str) or len(senha) < 6:
        return jsonify({"erro": "Campo 'senha' inválido (mínimo 6 caracteres)."}), 400

    conn = get_conn()
    cur = conn.cursor()

    # Checa se e-mail já existe
    cur.execute("SELECT id FROM users WHERE email = ?", (email.lower().strip(),))
    existing = cur.fetchone()
    if existing:
        return jsonify({"erro": "E-mail já cadastrado."}), 409

    # Hash da senha (não salvar senha em texto puro)
    senha_hash = generate_password_hash(senha)

    created_at = datetime.utcnow().isoformat() + "Z"

    try:
        cur.execute(
            "INSERT INTO users (nome, email, senha_hash, created_at) VALUES (?, ?, ?, ?)",
            (nome.strip(), email.lower().strip(), senha_hash, created_at),
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.Error as e:
        # Para debug em desenvolvimento você pode logar e retornar 500
        return jsonify({"erro": "Erro ao salvar usuário.", "detalhe": str(e)}), 500

    return jsonify(
        {
            "mensagem": "Usuário cadastrado com sucesso.",
            "usuario": {"id": user_id, "nome": nome.strip(), "email": email.lower().strip()},
        }
    ), 201

# Execução direta
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)