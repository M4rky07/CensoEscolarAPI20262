
from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService:

    @staticmethod
    def listar(pagina=1, por_pagina=20):

        # Conta os registros disponíveis
        total_registros = InstituicaoEnsinoRepository.contar()

        # Calcula quantos registros devem ser ignorados
        offset = (pagina - 1) * por_pagina

        # Busca os registros da página solicitada
        instituicoes = InstituicaoEnsinoRepository.listar(
            offset,
            por_pagina
        )

        # Calcula o total de páginas
        total_paginas = (
            total_registros + por_pagina - 1
        ) // por_pagina

        return {
            "dados": instituicoes,
            "paginacao": {
                "pagina_atual": pagina,
                "registros_por_pagina": por_pagina,
                "total_registros": total_registros,
                "total_paginas": total_paginas
            }
        }

    @staticmethod
    def buscar_por_id(id):
        return InstituicaoEnsinoRepository.buscar_por_id(id)

    @staticmethod
    def criar(data):
        return InstituicaoEnsinoRepository.criar(data)

    @staticmethod
    def atualizar(id, data):
        return InstituicaoEnsinoRepository.atualizar(id, data)

    @staticmethod
    def excluir(id):
        return InstituicaoEnsinoRepository.excluir(id)
