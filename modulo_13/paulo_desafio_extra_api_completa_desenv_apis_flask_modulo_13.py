# app.py
import os
import sqlite3
import re
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

from flask import Flask, g, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

# ---------- Config ----------
DB_PATH = os.environ.get("BLOG_DB_PATH", "blog.db")
JWT_SECRET = os.environ.get("BLOG_JWT_SECRET", "troque_esta_chave_para_producao")
JWT_ALGO = "HS256"
JWT_EXP_MINUTES = int(os.environ.get("BLOG_JWT_EXP_MINUTES", "60"))

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ---------- Database helpers ----------
def get_conn() -> sqlite3.Connection:
    conn = getattr(g, "_database", None)
    if conn is None:
        conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        g._database = conn
    return conn

@app.teardown_appcontext
def close_conn(exc):
    conn = getattr(g, "_database", None)
    if conn is not None:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Users
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
    # Posts
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    # Comments
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    conn.close()

# Initialize DB on import (handy for exercises)
init_db()

# ---------- Auth helpers ----------
def create_token(user_id: int) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXP_MINUTES),
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    # In PyJWT >= 2.x, jwt.encode returns a str
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_auth_header_token():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth.split(" ", 1)[1].strip()
    return None

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_auth_header_token()
        if not token:
            return jsonify({"erro": "Token ausente"}), 401
        payload = decode_token(token)
        if not payload:
            return jsonify({"erro": "Token inválido ou expirado"}), 401
        # attach user id to request context
        request.user_id = payload.get("sub")
        return f(*args, **kwargs)
    return decorated

# ---------- Routes: Auth ----------
@app.route("/auth/register", methods=["POST"])
def register():
    """
    POST /auth/register
    JSON: { "nome": "...", "email": "...", "senha": "..." }
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400
    data = request.get_json()
    nome: Optional[str] = data.get("nome")
    email: Optional[str] = data.get("email")
    senha: Optional[str] = data.get("senha")

    if not nome or not isinstance(nome, str) or len(nome.strip()) < 2:
        return jsonify({"erro": "Nome inválido (mínimo 2 caracteres)"}), 400
    if not email or not isinstance(email, str) or not EMAIL_REGEX.match(email):
        return jsonify({"erro": "Email inválido"}), 400
    if not senha or not isinstance(senha, str) or len(senha) < 6:
        return jsonify({"erro": "Senha inválida (mínimo 6 caracteres)"}), 400

    conn = get_conn()
    cur = conn.cursor()
    email_norm = email.lower().strip()
    cur.execute("SELECT id FROM users WHERE email = ?", (email_norm,))
    if cur.fetchone():
        return jsonify({"erro": "Email já cadastrado"}), 409

    senha_hash = generate_password_hash(senha)
    created_at = datetime.utcnow().isoformat() + "Z"
    try:
        cur.execute(
            "INSERT INTO users (nome, email, senha_hash, created_at) VALUES (?, ?, ?, ?)",
            (nome.strip(), email_norm, senha_hash, created_at),
        )
        conn.commit()
        user_id = cur.lastrowid
    except Exception as e:
        return jsonify({"erro": "Erro ao criar usuário", "detalhe": str(e)}), 500

    token = create_token(user_id)
    return jsonify({"mensagem": "Usuário criado", "usuario": {"id": user_id, "nome": nome.strip(), "email": email_norm}, "token": token}), 201

@app.route("/auth/login", methods=["POST"])
def login():
    """
    POST /auth/login
    JSON: { "email": "...", "senha": "..." }
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400
    data = request.get_json()
    email: Optional[str] = data.get("email")
    senha: Optional[str] = data.get("senha")
    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, senha_hash, nome, email FROM users WHERE email = ?", (email.lower().strip(),))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Credenciais inválidas"}), 401
    if not check_password_hash(row["senha_hash"], senha):
        return jsonify({"erro": "Credenciais inválidas"}), 401
    token = create_token(row["id"])
    return jsonify({"mensagem": "Login bem-sucedido", "token": token, "usuario": {"id": row["id"], "nome": row["nome"], "email": row["email"]}})

# ---------- Routes: Posts ----------
@app.route("/posts", methods=["POST"])
@jwt_required
def create_post():
    """
    POST /posts
    JSON: { "title": "...", "content": "..." }
    Auth required.
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400
    data = request.get_json()
    title: Optional[str] = data.get("title")
    content: Optional[str] = data.get("content")
    if not title or len(title.strip()) < 3:
        return jsonify({"erro": "Title inválido (mínimo 3 caracteres)"}), 400
    if not content or len(content.strip()) < 5:
        return jsonify({"erro": "Conteúdo inválido (mínimo 5 caracteres)"}), 400

    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat() + "Z"
    cur.execute("INSERT INTO posts (author_id, title, content, created_at) VALUES (?, ?, ?, ?)",
                (request.user_id, title.strip(), content.strip(), created_at))
    conn.commit()
    post_id = cur.lastrowid
    return jsonify({"mensagem": "Post criado", "post": {"id": post_id, "author_id": request.user_id, "title": title.strip(), "content": content.strip(), "created_at": created_at}}), 201

@app.route("/posts", methods=["GET"])
def list_posts():
    """
    GET /posts?page=1&per_page=10
    Public endpoint: list posts with pagination (most recent first).
    """
    page = int(request.args.get("page", "1") or 1)
    per_page = min(50, max(1, int(request.args.get("per_page", "10") or 10)))
    offset = (max(1, page) - 1) * per_page

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT p.id, p.title, p.content, p.created_at, p.updated_at, p.author_id, u.nome as author_name FROM posts p JOIN users u ON p.author_id = u.id ORDER BY p.created_at DESC LIMIT ? OFFSET ?", (per_page, offset))
    rows = cur.fetchall()
    posts = [dict(row) for row in rows]

    # Count total
    cur.execute("SELECT COUNT(1) as total FROM posts")
    total = cur.fetchone()["total"]
    return jsonify({"page": page, "per_page": per_page, "total": total, "posts": posts})

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT p.id, p.title, p.content, p.created_at, p.updated_at, p.author_id, u.nome as author_name FROM posts p JOIN users u ON p.author_id = u.id WHERE p.id = ?", (post_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Post não encontrado"}), 404
    return jsonify(dict(row))

@app.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required
def update_post(post_id: int):
    """
    PUT /posts/<post_id>
    Auth required. Only author can update.
    JSON: { "title": "...", "content": "..." } (either/both)
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Post não encontrado"}), 404
    if row["author_id"] != request.user_id:
        return jsonify({"erro": "Apenas o autor pode editar este post"}), 403

    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    updates = []
    params = []
    if title and len(title.strip()) >= 3:
        updates.append("title = ?")
        params.append(title.strip())
    if content and len(content.strip()) >= 5:
        updates.append("content = ?")
        params.append(content.strip())
    if not updates:
        return jsonify({"erro": "Nada para atualizar (title mínimo 3 chars, content mínimo 5 chars)"}), 400
    updates.append("updated_at = ?")
    params.append(datetime.utcnow().isoformat() + "Z")
    params.append(post_id)
    sql = "UPDATE posts SET " + ", ".join(updates) + " WHERE id = ?"
    cur.execute(sql, tuple(params))
    conn.commit()
    return jsonify({"mensagem": "Post atualizado"})

@app.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required
def delete_post(post_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Post não encontrado"}), 404
    if row["author_id"] != request.user_id:
        return jsonify({"erro": "Apenas o autor pode excluir este post"}), 403
    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    return jsonify({"mensagem": "Post excluído"})

# ---------- Routes: Comments ----------
@app.route("/posts/<int:post_id>/comments", methods=["POST"])
@jwt_required
def create_comment(post_id: int):
    """
    POST /posts/<post_id>/comments
    JSON: { "content": "..." }
    """
    if not request.is_json:
        return jsonify({"erro": "Conteúdo deve ser JSON"}), 400
    data = request.get_json()
    content: Optional[str] = data.get("content")
    if not content or len(content.strip()) < 1:
        return jsonify({"erro": "Conteúdo do comentário é obrigatório"}), 400

    conn = get_conn()
    cur = conn.cursor()
    # Ensure post exists
    cur.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cur.fetchone():
        return jsonify({"erro": "Post não encontrado"}), 404

    created_at = datetime.utcnow().isoformat() + "Z"
    cur.execute("INSERT INTO comments (post_id, author_id, content, created_at) VALUES (?, ?, ?, ?)",
                (post_id, request.user_id, content.strip(), created_at))
    conn.commit()
    comment_id = cur.lastrowid
    return jsonify({"mensagem": "Comentário criado", "comment": {"id": comment_id, "post_id": post_id, "author_id": request.user_id, "content": content.strip(), "created_at": created_at}}), 201

@app.route("/posts/<int:post_id>/comments", methods=["GET"])
def list_comments(post_id: int):
    """
    GET /posts/<post_id>/comments
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if not cur.fetchone():
        return jsonify({"erro": "Post não encontrado"}), 404
    cur.execute("SELECT c.id, c.content, c.created_at, c.author_id, u.nome as author_name FROM comments c JOIN users u ON c.author_id = u.id WHERE c.post_id = ? ORDER BY c.created_at ASC", (post_id,))
    rows = cur.fetchall()
    comments = [dict(r) for r in rows]
    return jsonify({"post_id": post_id, "comments": comments})

@app.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required
def delete_comment(comment_id: int):
    """
    DELETE /comments/<id>
    Only comment author or post author can delete.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT post_id, author_id FROM comments WHERE id = ?", (comment_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Comentário não encontrado"}), 404
    post_id = row["post_id"]
    comment_author = row["author_id"]
    # get post author
    cur.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,))
    post = cur.fetchone()
    post_author = post["author_id"] if post else None

    if request.user_id != comment_author and request.user_id != post_author:
        return jsonify({"erro": "Somente o autor do comentário ou o autor do post pode excluir"}), 403

    cur.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    return jsonify({"mensagem": "Comentário excluído"})

# ---------- Optional utility endpoints ----------
@app.route("/me", methods=["GET"])
@jwt_required
def me():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, created_at FROM users WHERE id = ?", (request.user_id,))
    row = cur.fetchone()
    if not row:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    return jsonify(dict(row))

# ---------- Run ----------
if __name__ == "__main__":
    # DEBUG apenas para desenvolvimento local
    app.run(host="0.0.0.0", port=5000, debug=True)