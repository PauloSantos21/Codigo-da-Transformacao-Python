from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/saudacao", methods=["GET"])
def saudacao():
    return app.response_class(
        response='{"mensagem": "Olá! Bem-vindo ao servidor Flask."}',
        mimetype="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    # debug=True apenas em desenvolvimento
    app.run(host="0.0.0.0", port=5000, debug=True)