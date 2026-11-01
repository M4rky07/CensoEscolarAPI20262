
from helpers.application import app

from controllers.InstituicaoEnsinoController import instituicao_ensino_bp
from controllers.IndexController import index_bp


app.register_blueprint(instituicao_ensino_bp)
app.register_blueprint(index_bp)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
