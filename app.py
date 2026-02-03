from flask import Flask, redirect, url_for
from app.controller.usuario import user_bp as usercontroller
from app.controller.home import home_bp as homecontroller
from app.controller.favorite import favorite_bp
from app.controller.teams import teams_bp
from app.models.usuario import db
import os, subprocess

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.sqlite3'

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'chave_generica_para_dev_local')

db.init_app(app)

app.register_blueprint(usercontroller, url_prefix="/pokedex/")
app.register_blueprint(homecontroller, url_prefix="/pokedex/")
app.register_blueprint(favorite_bp, url_prefix="/favorite")
app.register_blueprint(teams_bp, url_prefix="/teams")

@app.route('/')
def index():
    return redirect(url_for('home.home'))

def executar_preprocessamento():
    csv_ok = os.path.exists("app/data/pokemons.csv")
    imgs_ok = os.path.isdir("app/static/images/pokemons") and len(os.listdir("app/static/images/pokemons")) > 0

    if not csv_ok or not imgs_ok:
        print("\n[AVISO] Gerando CSV e imagens...\n")
        subprocess.run(
            ["python", os.path.join("app", "static", "py", "pre_processamento.py")],
            check=True
        )

executar_preprocessamento()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)