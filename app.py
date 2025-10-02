# app.py
import os
from flask import Flask, session
from backend.config import APARELHOS
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Importa e registra os blueprints
    from blueprints.inicio import inicio_bp
    from blueprints.gerenciamento import gerenciamento_bp
    from blueprints.voz_bp import voz_bp

    app.register_blueprint(inicio_bp)
    app.register_blueprint(gerenciamento_bp)
    app.register_blueprint(voz_bp, url_prefix='/voz')
    # Inicializa o estado dos dispositivos na sessão na primeira requisição
    @app.before_request
    def initialize_session():
        if "dispositivos_estado" not in session:
            session["dispositivos_estado"] = {
                comodo: {chave: False for chave in APARELHOS[comodo]}
                for comodo in APARELHOS
            }
        if "comodo_selecionado" not in session:
            session["comodo_selecionado"] = "sala"

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)