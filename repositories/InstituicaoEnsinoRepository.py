
from helpers.database import get_connection


class InstituicaoEnsinoRepository:


    @staticmethod
    def contar():
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM instituicoesensino
                WHERE excluido = 0
            """)

            return cursor.fetchone()[0]

        finally:
            connection.close()

    @staticmethod
    def listar(offset, por_pagina):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                       co_uf, no_municipio, co_municipio, nu_ano_censo,
                       qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                       qt_mat_prof, qt_mat_eja, qt_mat_esp
                FROM instituicoesensino
                WHERE excluido = 0
                ORDER BY id ASC
                LIMIT ? OFFSET ?
            """, (por_pagina, offset))

            return [dict(row) for row in cursor.fetchall()]

        finally:
            connection.close()

    @staticmethod
    def buscar_por_id(id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                       co_uf, no_municipio, co_municipio, nu_ano_censo,
                       qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                       qt_mat_prof, qt_mat_eja, qt_mat_esp
                FROM instituicoesensino
                WHERE id = ? AND excluido = 0
            """, (id,))

            row = cursor.fetchone()

            return dict(row) if row else None

        finally:
            connection.close()

    @staticmethod
    def criar(data):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO instituicoesensino (
                    no_entidade, co_entidade, no_uf, sg_uf,
                    co_uf, no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["no_entidade"],
                data["co_entidade"],
                data["no_uf"],
                data["sg_uf"],
                data["co_uf"],
                data["no_municipio"],
                data["co_municipio"],
                data["nu_ano_censo"],
                data["qt_mat_bas"],
                data["qt_mat_inf"],
                data["qt_mat_fund"],
                data["qt_mat_med"],
                data["qt_mat_prof"],
                data["qt_mat_eja"],
                data["qt_mat_esp"]
            ))

            novo_id = cursor.lastrowid
            connection.commit()

            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                       co_uf, no_municipio, co_municipio, nu_ano_censo,
                       qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                       qt_mat_prof, qt_mat_eja, qt_mat_esp
                FROM instituicoesensino
                WHERE id = ?
            """, (novo_id,))

            return dict(cursor.fetchone())

        finally:
            connection.close()

    @staticmethod
    def atualizar(id, data):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE instituicoesensino
                SET no_entidade = ?,
                    co_entidade = ?,
                    no_uf = ?,
                    sg_uf = ?,
                    co_uf = ?,
                    no_municipio = ?,
                    co_municipio = ?,
                    nu_ano_censo = ?,
                    qt_mat_bas = ?,
                    qt_mat_inf = ?,
                    qt_mat_fund = ?,
                    qt_mat_med = ?,
                    qt_mat_prof = ?,
                    qt_mat_eja = ?,
                    qt_mat_esp = ?
                WHERE id = ? AND excluido = 0
            """, (
                data["no_entidade"],
                data["co_entidade"],
                data["no_uf"],
                data["sg_uf"],
                data["co_uf"],
                data["no_municipio"],
                data["co_municipio"],
                data["nu_ano_censo"],
                data["qt_mat_bas"],
                data["qt_mat_inf"],
                data["qt_mat_fund"],
                data["qt_mat_med"],
                data["qt_mat_prof"],
                data["qt_mat_eja"],
                data["qt_mat_esp"],
                id
            ))

            if cursor.rowcount == 0:
                return None

            connection.commit()

            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                       co_uf, no_municipio, co_municipio, nu_ano_censo,
                       qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                       qt_mat_prof, qt_mat_eja, qt_mat_esp
                FROM instituicoesensino
                WHERE id = ? AND excluido = 0
            """, (id,))

            return dict(cursor.fetchone())

        finally:
            connection.close()

    @staticmethod
    def excluir(id):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE instituicoesensino
                SET excluido = 1
                WHERE id = ? AND excluido = 0
            """, (id,))

            if cursor.rowcount == 0:
                return False

            connection.commit()

            return True

        finally:
            connection.close()
