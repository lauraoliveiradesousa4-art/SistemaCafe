
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder="static")
CORS(app)

def conectar():
    conexao = sqlite3.connect("cafe.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def iniciar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL
            )
        """)

        total = conexao.execute(
            "SELECT COUNT(*) FROM produtos"
        ).fetchone()[0]

        if total == 0:
            produtos = [
                ("Café expresso", "Bebidas", 5.0, 30),
                ("Cappuccino", "Bebidas", 9.0, 20),
                ("Chocolate quente", "Bebidas", 8.0, 15),
                ("Suco natural", "Bebidas", 7.0, 20),
                ("Pão de queijo", "Salgados", 4.0, 40),
                ("Coxinha", "Salgados", 6.0, 25),
                ("Sanduíche", "Salgados", 12.0, 15),
                ("Bolo de chocolate", "Doces", 8.0, 12),
                ("Brownie", "Doces", 7.0, 18),
                ("Cookie", "Doces", 5.0, 30)
            ]

            conexao.executemany("""
                INSERT INTO produtos
                (nome, categoria, preco, estoque)
                VALUES (?, ?, ?, ?)
            """, produtos)

def validar(dados):
    if not isinstance(dados, dict):
        return "Envie um objeto JSON válido."

    for campo in ["nome", "categoria", "preco", "estoque"]:
        if campo not in dados:
            return "Preencha todos os campos."

    if not isinstance(dados["nome"], str) or not dados["nome"].strip():
        return "Nome é obrigatório."

    if not isinstance(dados["categoria"], str) or not dados["categoria"].strip():
        return "Categoria é obrigatória."

    try:
        preco = float(dados["preco"])
        estoque = int(dados["estoque"])
        if preco < 0 or estoque < 0:
            return "Preço e estoque não podem ser negativos."
    except (ValueError, TypeError, OverflowError):
        return "Preço ou estoque inválido."

    return None

@app.route("/")
def pagina():
    return send_from_directory("static", "index.html")

@app.route("/api/produtos", methods=["GET"])
def listar():
    with conectar() as conexao:
        produtos = conexao.execute(
            "SELECT * FROM produtos ORDER BY id"
        ).fetchall()
    return jsonify([dict(p) for p in produtos])

@app.route("/api/produtos", methods=["POST"])
def cadastrar():
    dados = request.get_json(silent=True)
    erro = validar(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    with conectar() as conexao:
        cursor = conexao.execute("""
            INSERT INTO produtos (nome, categoria, preco, estoque)
            VALUES (?, ?, ?, ?)
        """, (
            dados["nome"].strip(),
            dados["categoria"].strip(),
            float(dados["preco"]),
            int(dados["estoque"])
        ))

        novo_id = cursor.lastrowid

    return jsonify({
        "mensagem": "Produto cadastrado!",
        "id": novo_id
    }), 201

@app.route("/api/produtos/<int:id>", methods=["PUT"])
def editar(id):
    dados = request.get_json(silent=True)
    erro = validar(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    with conectar() as conexao:
        cursor = conexao.execute("""
            UPDATE produtos
            SET nome=?, categoria=?, preco=?, estoque=?
            WHERE id=?
        """, (
            dados["nome"].strip(),
            dados["categoria"].strip(),
            float(dados["preco"]),
            int(dados["estoque"]),
            id
        ))

        if cursor.rowcount == 0:
            return jsonify({"erro": "Produto não encontrado."}), 404

    return jsonify({"mensagem": "Produto atualizado!"})

@app.route("/api/produtos/<int:id>", methods=["DELETE"])
def excluir(id):
    with conectar() as conexao:
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE id=?", (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"erro": "Produto não encontrado."}), 404

    return jsonify({"mensagem": "Produto excluído!"})

if __name__ == "__main__":
    iniciar_banco()
    app.run(debug=True, port=5000)
