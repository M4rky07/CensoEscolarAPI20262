from flask import Flask, request

from models.instituicaoensino import InstituicaoEnsino
from models.usuario import Usuario

from helpers.file.json import read, write


app = Flask(__name__)



def listarInstituicoes():

    dataset = read("instituicoes.json")

    instituicoesEnsino = [
        InstituicaoEnsino(
            int(row["id"]),
            row["no_entidade"],
            row["co_entidade"],
            row["qt_mat_bas"]
        )
        for row in dataset
    ]

    return instituicoesEnsino


def salvarInstituicoes(instituicoesEnsino):

    dataset = [
        instituicaoEnsino.toDict()
        for instituicaoEnsino in instituicoesEnsino
    ]

    write("instituicoes.json", dataset)


def listarUsuarios():

    dataset = read("usuarios.json")

    usuarios = [
        Usuario(
            int(row["id"]),
            row["nome"],
            row["email"],
            row["senha"]
        )
        for row in dataset
    ]

    return usuarios


def salvarUsuarios(usuarios):

    dataset = [
        usuario.toDict()
        for usuario in usuarios
    ]

    write("usuarios.json", dataset)



@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200



@app.get("/instituicoesensino")
def getAllInstituicoes():

    instituicoesEnsino = listarInstituicoes()

    coEntidade = request.args.get("co_entidade")

    if coEntidade is not None:

        instituicoesEnsinoResponse = [
            instituicaoEnsino.toDict()
            for instituicaoEnsino in instituicoesEnsino
            if str(instituicaoEnsino.co_entidade) == coEntidade
        ]

    else:

        instituicoesEnsinoResponse = [
            instituicaoEnsino.toDict()
            for instituicaoEnsino in instituicoesEnsino
        ]

    return instituicoesEnsinoResponse, 200



@app.get("/instituicoesensino/<int:id>")
def getByIdInstituicoes(id):

    instituicoesEnsino = listarInstituicoes()

    for instituicaoEnsino in instituicoesEnsino:

        if instituicaoEnsino.id == id:
            return instituicaoEnsino.toDict(), 200

    return {"erro": "Instituição não encontrada"}, 404


@app.post("/instituicoesensino")
def postInstituicoes():

    data = request.get_json()

    if not data:
        return {"erro": "Dados não enviados"}, 400

    no_entidade = data.get("no_entidade")
    co_entidade = data.get("co_entidade")
    qt_mat_bas = data.get("qt_mat_bas")

    if no_entidade is None or co_entidade is None or qt_mat_bas is None:
        return {
            "erro": "Informe no_entidade, co_entidade e qt_mat_bas"
        }, 400

    instituicoesEnsino = listarInstituicoes()

    if instituicoesEnsino:

        novoId = max(
            instituicao.id
            for instituicao in instituicoesEnsino
        ) + 1

    else:
        novoId = 1

    novaInstituicao = InstituicaoEnsino(
        novoId,
        no_entidade,
        co_entidade,
        qt_mat_bas
    )

    instituicoesEnsino.append(novaInstituicao)

    salvarInstituicoes(instituicoesEnsino)

    return novaInstituicao.toDict(), 201


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):

    instituicoesEnsino = listarInstituicoes()

    instituicaoEncontrada = None

    for instituicaoEnsino in instituicoesEnsino:

        if instituicaoEnsino.id == id:
            instituicaoEncontrada = instituicaoEnsino
            break

    if instituicaoEncontrada is None:
        return {"erro": "Instituição não encontrada"}, 404

    data = request.get_json()

    if not data:
        return {"erro": "Dados não enviados"}, 400

    no_entidade = data.get("no_entidade")
    co_entidade = data.get("co_entidade")
    qt_mat_bas = data.get("qt_mat_bas")

    if no_entidade is None or co_entidade is None or qt_mat_bas is None:
        return {
            "erro": "Informe no_entidade, co_entidade e qt_mat_bas"
        }, 400

    instituicaoEncontrada.no_entidade = no_entidade
    instituicaoEncontrada.co_entidade = co_entidade
    instituicaoEncontrada.qt_mat_bas = qt_mat_bas

    salvarInstituicoes(instituicoesEnsino)

    return instituicaoEncontrada.toDict(), 200


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):

    instituicoesEnsino = listarInstituicoes()

    instituicaoEncontrada = None

    for instituicaoEnsino in instituicoesEnsino:

        if instituicaoEnsino.id == id:
            instituicaoEncontrada = instituicaoEnsino
            break

    if instituicaoEncontrada is None:
        return {"erro": "Instituição não encontrada"}, 404

    instituicoesEnsino.remove(instituicaoEncontrada)

    salvarInstituicoes(instituicoesEnsino)

    return {
        "mensagem": "Instituição excluída com sucesso"
    }, 200


@app.get("/usuarios")
def getAllUsuarios():

    usuarios = listarUsuarios()

    usuariosResponse = [
        usuario.toDict()
        for usuario in usuarios
    ]

    return usuariosResponse, 200


def getByIdUsuario(id):

    usuarios = listarUsuarios()

    for usuario in usuarios:

        if usuario.id == id:
            return usuario.toDict(), 200

    return {"erro": "Usuário não encontrado"}, 404


@app.post("/usuarios")
def postUsuario():

    data = request.get_json()

    if not data:
        return {"erro": "Dados não enviados"}, 400

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if nome is None or email is None or senha is None:
        return {
            "erro": "Informe nome, email e senha"
        }, 400

    usuarios = listarUsuarios()

    if usuarios:

        novoId = max(
            usuario.id
            for usuario in usuarios
        ) + 1

    else:
        novoId = 1

    novoUsuario = Usuario(
        novoId,
        nome,
        email,
        senha
    )

    usuarios.append(novoUsuario)

    salvarUsuarios(usuarios)

    return novoUsuario.toDict(), 201


@app.put("/usuarios/<int:id>")
def putUsuario(id):

    usuarios = listarUsuarios()

    usuarioEncontrado = None

    for usuario in usuarios:

        if usuario.id == id:
            usuarioEncontrado = usuario
            break

    if usuarioEncontrado is None:
        return {"erro": "Usuário não encontrado"}, 404

    data = request.get_json()

    if not data:
        return {"erro": "Dados não enviados"}, 400

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if nome is None or email is None or senha is None:
        return {
            "erro": "Informe nome, email e senha"
        }, 400

    usuarioEncontrado.nome = nome
    usuarioEncontrado.email = email
    usuarioEncontrado.senha = senha

    salvarUsuarios(usuarios)

    return usuarioEncontrado.toDict(), 200


@app.delete("/usuarios/<int:id>")
def deleteUsuario(id):

    usuarios = listarUsuarios()

    usuarioEncontrado = None

    for usuario in usuarios:

        if usuario.id == id:
            usuarioEncontrado = usuario
            break

    if usuarioEncontrado is None:
        return {"erro": "Usuário não encontrado"}, 404

    usuarios.remove(usuarioEncontrado)

    salvarUsuarios(usuarios)

    return {
        "mensagem": "Usuário excluído com sucesso"
    }, 200

def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()