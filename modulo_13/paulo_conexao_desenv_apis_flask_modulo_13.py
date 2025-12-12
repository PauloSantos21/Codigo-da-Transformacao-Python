# app.py
from flask import Flask, request, jsonify, g, Response
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from typing import Optional

DB_PATH = "clientes.db"
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False  # mantém a ordem dos campos no JSON (opcional)

# -----------------------
# Banco de dados
# -----------------------
def get_conn() -> sqlite3.Connection:
    """
    Retorna uma conexão por contexto (g). Usa row_factory para acessar colunas por nome.
    """
    conn = getattr(g, "_database", None)
    if conn is None:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
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

# Inicializa DB ao importar/executar (bom para exercícios)
init_db()

# -----------------------
# Rotas
# -----------------------
@app.route("/saudacao", methods=["GET"])
def saudacao():
    # Retorna JSON com charset para garantir acentuação correta em alguns browsers
    return Response(
        '{"mensagem": "Olá! Bem-vindo ao servidor Flask."}',
        content_type="application/json; charset=utf-8",
        status=200,
    )

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    """
    POST /cadastrar
    JSON esperado:
    {
      "nome": "Fulano",
      "email": "fulano@example.com",
      "senha": "minhaSenhaSegura"
    }
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400

    data = request.get_json()

    nome: Optional[str] = data.get("nome")
    email: Optional[str] = data.get("email")
    senha: Optional[str] = data.get("senha")

    # Validações
    if not nome or not isinstance(nome, str) or len(nome.strip()) < 2:
        return jsonify({"erro": "Campo 'nome' inválido (mínimo 2 caracteres)."}), 400

    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email):
        return jsonify({"erro": "Campo 'email' inválido."}), 400

    if not senha or not isinstance(senha, str) or len(senha) < 6:
        return jsonify({"erro": "Campo 'senha' inválido (mínimo 6 caracteres)."}), 400

    conn = get_conn()
    cur = conn.cursor()

    # Normaliza email
    email_norm = email.lower().strip()

    # Checa se e-mail já existe
    cur.execute("SELECT id FROM users WHERE email = ?", (email_norm,))
    existing = cur.fetchone()
    if existing:
        return jsonify({"erro": "E-mail já cadastrado."}), 409

    senha_hash = generate_password_hash(senha)
    created_at = datetime.utcnow().isoformat() + "Z"

    try:
        cur.execute(
            "INSERT INTO users (nome, email, senha_hash, created_at) VALUES (?, ?, ?, ?)",
            (nome.strip(), email_norm, senha_hash, created_at),
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.Error as e:
        return jsonify({"erro": "Erro ao salvar usuário.", "detalhe": str(e)}), 500

    return (
        jsonify(
            {
                "mensagem": "Usuário cadastrado com sucesso.",
                "usuario": {"id": user_id, "nome": nome.strip(), "email": email_norm},
            }
        ),
        201,
    )

@app.route("/users", methods=["GET"])
def list_users():
    """
    GET /users?page=1&per_page=10
    Retorna usuários (sem senha_hash) com paginação simples.
    """
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")
    try:
        page_i = max(1, int(page))
        per_page_i = min(100, max(1, int(per_page)))
    except ValueError:
        return jsonify({"erro": "Parâmetros de paginação inválidos."}), 400

    offset = (page_i - 1) * per_page_i

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nome, email, created_at FROM users ORDER BY id DESC LIMIT ? OFFSET ?",
        (per_page_i, offset),
    )
    rows = cur.fetchall()
    users = [dict(row) for row in rows]

    # Conta total (opcional)
    cur.execute("SELECT COUNT(1) as total FROM users")
    total = cur.fetchone()["total"]

    return jsonify({"page": page_i, "per_page": per_page_i, "total": total, "users": users})

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """
    GET /users/<id> — retorna o usuário sem a senha_hash
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, created_at FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Usuário não encontrado."}), 404
    return jsonify(dict(row))

# Rota auxiliar para desenvolvimento: exportar CSV dos usuários (sem senha_hash)
@app.route("/export/csv", methods=["GET"])
def export_csv():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, created_at FROM users ORDER BY id")
    rows = cur.fetchall()

    # Monta CSV simples
    output_lines = ["id,nome,email,created_at"]
    for r in rows:
        # Escapa vírgulas básicas
        nome = r["nome"].replace('"', '""')
        email = r["email"]
        output_lines.append(f'{r["id"]},"{nome}",{email},{r["created_at"]}')

    csv_text = "\n".join(output_lines)
    return Response(csv_text, content_type="text/csv; charset=utf-8")

# -----------------------
# Execução
# -----------------------
if __name__ == "__main__":
    # debug=True apenas em ambiente de desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)