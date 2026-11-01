
from flask import Blueprint, request, jsonify
from sqlite3 import IntegrityError
from marshmallow import ValidationError

from models.instituicaoensino import InstituicaoEnsinoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService
from helpers.logger import logger


instituicaoEnsinoSchema = InstituicaoEnsinoSchema()

instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)


instituicao_ensino_bp = Blueprint(
    'instituicaoensino',
    __name__,
    url_prefix='/instituicoesensino'
)


# GET - Listar instituições
# GET - Listar instituições
@instituicao_ensino_bp.get("/")
def get_all_instituicoes():

    try:
        pagina = request.args.get("pagina", default=1, type=int)
        por_pagina = request.args.get("por_pagina", default=20, type=int)

        if pagina < 1 or por_pagina < 1:
            return jsonify({
                "erro": "Os parâmetros pagina e por_pagina devem ser maiores que zero"
            }), 400

        if por_pagina > 100:
            return jsonify({
                "erro": "O limite máximo é de 100 registros por página"
            }), 400

        logger.info(
            f"Listando instituições - Página: {pagina}, "
            f"Registros por página: {por_pagina}"
        )

        instituicoes = InstituicaoEnsinoService.listar(
            pagina=pagina,
            por_pagina=por_pagina
        )

        logger.info("Finalizando o processamento da listagem")

        return jsonify(instituicoes), 200

    except Exception as erro:
        logger.exception("Erro ao listar instituições")

        return jsonify({
            "erro": "Erro interno ao listar instituições"
        }), 500


# GET - Buscar instituição por ID
@instituicao_ensino_bp.get("/<int:id>")
def get_instituicao_by_id(id):

    logger.info(f"Buscando instituição de ID {id}")

    instituicao = InstituicaoEnsinoService.buscar_por_id(id)

    if instituicao is None:
        return jsonify({
            "mensagem": "Instituição de ensino não encontrada"
        }), 404

    return jsonify(instituicao), 200


# POST - Cadastrar instituição
@instituicao_ensino_bp.post("/")
def post_instituicao():

    try:
        data = instituicaoEnsinoSchema.load(request.get_json())

        instituicao = InstituicaoEnsinoService.criar(data)

        logger.info("Instituição cadastrada com sucesso")

        return jsonify(instituicao), 201

    except ValidationError as err:
        return jsonify({
            "erro": "Dados inválidos",
            "campos": err.messages
        }), 400

    except IntegrityError:
        return jsonify({
            "erro": "Já existe uma instituição com esse código INEP"
        }), 409


# PUT - Atualizar instituição
@instituicao_ensino_bp.put("/<int:id>")
def put_instituicao(id):

    try:
        data = instituicaoEnsinoSchema.load(request.get_json())

        instituicao = InstituicaoEnsinoService.atualizar(id, data)

        if instituicao is None:
            return jsonify({
                "mensagem": "Instituição de ensino não encontrada"
            }), 404

        logger.info(f"Instituição {id} atualizada com sucesso")

        return jsonify(instituicao), 200

    except ValidationError as err:
        return jsonify({
            "erro": "Dados inválidos",
            "campos": err.messages
        }), 400

    except IntegrityError:
        return jsonify({
            "erro": "Já existe uma instituição com esse código INEP"
        }), 409


# DELETE - Excluir instituição
@instituicao_ensino_bp.delete("/<int:id>")
def delete_instituicao(id):

    excluida = InstituicaoEnsinoService.excluir(id)

    if not excluida:
        return jsonify({
            "mensagem": "Instituição de ensino não encontrada"
        }), 404

    logger.info(f"Instituição {id} excluída com sucesso")

    return jsonify({
        "mensagem": "Instituição excluída com sucesso"
    }), 200
