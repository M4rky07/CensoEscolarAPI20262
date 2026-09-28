from flask import Flask, request

from models.instituicaoensino import InstituicaoEnsino
from helpers.file.json import read
from helpers.database import get_connection


def listar():
    # Ler o arquivo json.
    dataset = read("instituicoes.json")
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino


app = Flask(__name__)


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200

# /instituicoesensino?co_inep=123456


@app.get("/instituicoesensino")
def getAllInstituicoes():
    insituicoesEnsinoReponse = []
    # Abrir a conexão com o banco de dados.
    connection = get_connection()
    cursor = connection.cursor()
    # Executar as DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino')
    dataset = cursor.fetchall()

    for row in dataset:
        print(type(row))
    # Transformação dos dados
    # Responder/retorna os dados ao cliente

    return insituicoesEnsinoReponse, 200


@app.get("/instituicoesensino/<id>")
def getByIdInstituicoes(id):
    Connection = get_connection()
    cursor = Connection.cursor()

    cursor.execute( "SELECT * FROM tb_instituicao_ensino WHERE id = ?", (id,))

    row = cursor.fetchone()

    if row is None:
        return {"Erro": "Instituição não encontrada"}, 404

    instituicao = {
        "id" : [0],
        "no_entidade": row[1],
        "co_entidade": row[2],
        "qt_mat_bas": row[3]

    }

    return instituicao, 200





@app.post("/instituicoesensino")
def postInstituicoes():
    data = request.get_json()

    id = data.get("id")
    no_entidade = data.get("no_entidade")
    co_entidade = data.get("co_entidade")
    qt_mat_bas = data.get("qt_mat_bas")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tb_instituicao_ensino (id, no_entidade, co_entidade, qt_mat_bas)
        VALUES (?, ?, ?, ?)
    """, (id, no_entidade, co_entidade, qt_mat_bas))

    connection.commit()

    instituicao = {
        "id": id,
        "no_entidade": no_entidade,
        "co_entidade": co_entidade,
        "qt_mat_bas": qt_mat_bas
    }

    return instituicao, 201


@app.put("/instituicoesensino/<id>")
def putInstituicoes(id):

    data = request.get_json()

    no_entidade = data.get("no_entidade")
    co_entidade = data.get("co_entidade")
    qt_mat_bas = data.get("qt_mat_bas")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tb_instituicao_ensino
        SET no_entidade = ?,
            co_entidade = ?,
            qt_mat_bas = ?
        WHERE id = ?
    """, (
        no_entidade,
        co_entidade,
        qt_mat_bas,
        id
    ))

    connection.commit()

    if cursor.rowcount == 0:
        return {"erro": "Instituição não encontrada"}, 404

    instituicao = {
        "id": id,
        "no_entidade": no_entidade,
        "co_entidade": co_entidade,
        "qt_mat_bas": qt_mat_bas
    }

    return instituicao, 200
    


@app.delete("/instituicoesensino/<id>")
def deleteInstituicoes(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tb_instituicao_ensino WHERE id = ?",
        (id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        return {"erro": "Instituição não encontrada"}, 404

    return {"mensagem": "Instituição excluída com sucesso"}, 200


def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()
