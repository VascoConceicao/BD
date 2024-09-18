#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
import psycopg
import random
from datetime import datetime

from logging.config import dictConfig
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://saude:saude@postgres/saude")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,  # If True don’t start transactions automatically.
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    # check=ConnectionPool.check_connection,
    name="postgres_pool",
    timeout=5,
)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger


def is_decimal(s):
    """Returns True if string is a parseable float number."""
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_date(string):
    try:
        datetime.strptime(string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_time(string):
    try:
        datetime.strptime(string, "%H:%M:%S")
        return True
    except ValueError:
        return False
        
@app.route("/", methods=("GET",))
def lista_clinicas():

    with pool.connection() as conn:
        with conn.cursor() as cur:
            clinicas = cur.execute(
                """
                SELECT nome, morada
                FROM clinica
                ORDER BY nome DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(clinicas), 200

@app.route("/c/<clinica>/", methods=("GET",))
def lista_especialidades_clinica(clinica):

    if len(clinica) > 80:
        return jsonify({"message": "Nome da clínica tem menos de 80 caracteres.", "status": "error"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            especialidades = cur.execute(
                """
                SELECT DISTINCT especialidade
                FROM consulta c JOIN medico USING (nif)
                WHERE c.nome = %(clinica)s;
                """,
                {"clinica": clinica},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(especialidades), 200

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def lista_medicos_especialidade_clinica(clinica, especialidade):

    if len(clinica) > 80:
        return jsonify({"message": "Nome da clínica tem menos de 80 caracteres.", "status": "error"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            medicos = cur.execute(
                """
                SELECT nome, data, hora
                FROM (
                    SELECT m.nome, d.data, h.hora, ROW_NUMBER() OVER(PARTITION BY m.nome ORDER BY d.data, h.hora) AS row_number
                    FROM medico m CROSS JOIN (SELECT DISTINCT data FROM consulta) d CROSS JOIN (SELECT DISTINCT hora FROM consulta) h JOIN trabalha t ON (EXTRACT(DOW FROM d.data) = t.dia_da_semana AND t.nif = m.nif)
                    WHERE m.especialidade = %(especialidade)s 
                      AND t.nome = %(clinica)s 
                      AND d.data > NOW() 
                      AND NOT EXISTS (
                          SELECT 1
                          FROM consulta c
                          WHERE c.nif = m.nif 
                            AND c.nome = t.nome 
                            AND c.data = d.data 
                            AND c.hora = h.hora
                      )
                ) AS subquery
                WHERE row_number <= 3;
                """,
                {"clinica": clinica, "especialidade": especialidade},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")
            medicos = [(nome, data.strftime("%Y-%m-%d"), hora.strftime("%H:%M:%S")) for nome, data, hora in medicos]
    return jsonify(medicos), 200

@app.route("/a/<clinica>/registar/", methods=("PUT", "POST",))
def regista_consulta_clinica(clinica):

    if len(clinica) > 80:
        return jsonify({"message": "Nome da clínica tem menos de 80 caracteres.", "status": "error"}), 400
    
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")
    
    error = ""
    ok_data_hora = 1
    
    if not paciente:
        error += "Paciente is required. "
    if not is_decimal(paciente):
        error += "Paciente is required to be decimal. "

    if not medico:
        error += "Medico is required. "
    if not is_decimal(medico):
        error += "Medico is required to be decimal. "

    if not data:
        ok_data_hora = 0
        error += "Data is required. "
    if not is_date(data):
        ok_data_hora = 0
        error += "Data invalid format: YYYY-MM-DDq. "

    if not hora:
        ok_data_hora = 0
        error += "Hora is required. "
    if not is_time(hora):
        ok_data_hora = 0
        error += "Hora invalid format: HH:MM:SS. "

    if ok_data_hora:
        consulta_datetime = datetime.strptime(data + ' ' + hora, '%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
    
        if consulta_datetime < current_datetime:
            error += "Consulta não pode ser marcada, porque essa data é no passado. "

    if error != "":
        return jsonify({"message": error, "status": "error"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ssn
                FROM paciente
                WHERE ssn = %(paciente)s;
                """,
                {"paciente": paciente},
            )
            if not cur.fetchone():
                return jsonify({"message": "Paciente não existe.", "status": "error"}), 400
                
            cur.execute(
                """
                SELECT nif
                FROM medico
                WHERE nif = %(medico)s;
                """,
                {"medico": medico},
            )
            if not cur.fetchone():
                return jsonify({"message": "Médico não existe.", "status": "error"}), 400
                
            cur.execute(
                """
                SELECT id
                FROM consulta
                ORDER BY id DESC
                LIMIT 1;
                """
            )
            id_curr = cur.fetchone()
            id = int(id_curr[0]) + 1z
            try:
                cur.execute(
                    """
                    INSERT INTO consulta (id, ssn, nif, nome, data, hora)
                    VALUES(%(id)s, %(paciente)s, %(medico)s, %(clinica)s, %(data)s, %(hora)s);
                    """,
                    {"id": id, "paciente": paciente, "medico": medico, "clinica": clinica, "data": data, "hora": hora},
                )
            except psycopg.Error as e:
                error_message = str(e)
                if "consulta_ssn_data_hora_key" in error_message:
                    return jsonify({"message": "O paciente já tem uma marcação nesse horário.", "status": "error"}), 400
                elif "consulta_nif_data_hora_key" in error_message:
                    return jsonify({"message": "O médico já tem uma marcação nesse horário.", "status": "error"}), 400
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify({"message": "Consulta registada com sucesso.", "status": "success"}), 200

@app.route("/a/<clinica>/cancelar/", methods=("DELETE", "POST",))
def cancela_consulta_clinica(clinica):

    if len(clinica) > 80:
        return jsonify({"message": "Nome da clínica tem menos de 80 caracteres.", "status": "error"}), 400
        
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")
    
    error = ""
    ok_data_hora = 1
    
    if not paciente:
        error += "Paciente is required. "
    if not is_decimal(paciente):
        error += "Paciente is required to be decimal. "

    if not medico:
        error += "Medico is required. "
    if not is_decimal(medico):
        error += "Medico is required to be decimal. "

    if not data:
        ok_data_hora = 0
        error += "Data is required. "
    if not is_date(data):
        ok_data_hora = 0
        error += "Data invalid format: YYYY-MM-DDq. "

    if not hora:
        ok_data_hora = 0
        error += "Hora is required. "
    if not is_time(hora):
        ok_data_hora = 0
        error += "Hora invalid format: HH:MM:SS. "

    if ok_data_hora:
        consulta_datetime = datetime.strptime(data + ' ' + hora, '%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
    
        if consulta_datetime < current_datetime:
            error += "Consulta já foi realizada. "

    if error != "":
        return jsonify({"message": error, "status": "error"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ssn
                FROM paciente
                WHERE ssn = %(paciente)s;
                """,
                {"paciente": paciente},
            )
            if not cur.fetchone():
                return jsonify({"message": "Paciente não existe.", "status": "error"}), 400
                
            cur.execute(
                """
                SELECT nif
                FROM medico
                WHERE nif = %(medico)s;
                """,
                {"medico": medico},
            )
            if not cur.fetchone():
                return jsonify({"message": "Médico não existe.", "status": "error"}), 400

            cur.execute(
                """
                SELECT * FROM consulta
                WHERE ssn = %(paciente)s AND nif = %(medico)s AND data = %(data)s AND hora = %(hora)s;
                """,
                {"paciente": paciente, "medico": medico, "clinica": clinica, "data": data, "hora": hora},
            )
            if not cur.fetchone():
                return jsonify({"message": "Consulta não existe.", "status": "error"}), 400

            cur.execute(
                """
                DELETE FROM consulta
                WHERE ssn = %(paciente)s AND nif = %(medico)s AND data = %(data)s AND hora = %(hora)s;
                """,
                {"paciente": paciente, "medico": medico, "clinica": clinica, "data": data, "hora": hora},
            )
    
            log.debug(f"Found {cur.rowcount} rows.")
            
        return jsonify({"message": "Consulta cancelada com sucesso.", "status": "success"}), 200

if __name__ == "__main__":
    app.run()