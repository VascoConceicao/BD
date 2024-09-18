import os
import psycopg
import random
from datetime import datetime

from logging.config import dictConfig
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://saude:saude@postgres/saude")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": False,
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
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

    return jsonify(clinicas), 200

@app.route("/c/<clinica>/", methods=("GET",))
def lista_especialidades_clinica(clinica):

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM clinica
                WHERE nome = %(clinica)s;
                """,
                {"clinica": clinica},
            )
                
            if not cur.fetchone():
                return jsonify({"message": "Clínica não existe.", "status": "404 NOT FOUND"}), 404
            
            especialidades = cur.execute(
                """
                SELECT DISTINCT especialidade
                FROM consulta c JOIN medico USING (nif)
                WHERE c.nome = %(clinica)s;
                """,
                {"clinica": clinica},
            ).fetchall()
        
    return jsonify(especialidades), 200

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def lista_medicos_especialidade_clinica(clinica, especialidade):

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM clinica
                WHERE nome = %(clinica)s;
                """,
                {"clinica": clinica},
            )

            if not cur.fetchone():
                return jsonify({"message": "Clínica não existe.", "status": "404 NOT FOUND"}), 404
            
            cur.execute(
                """
                SELECT c.nome, m.especialidade
                FROM consulta c JOIN medico m USING (nif)
                WHERE c.nome = %(clinica)s AND especialidade = %(especialidade)s;
                """,
                {"clinica": clinica, "especialidade": especialidade},
            )
            
            if not cur.fetchone():
                return jsonify({"message": "Especialidade não existe.", "status": "404 NOT FOUND"}), 404
                
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
            
            medicos = [(nome, data.strftime("%Y-%m-%d"), hora.strftime("%H:%M:%S")) for nome, data, hora in medicos]
    return jsonify(medicos), 200

@app.route("/a/<clinica>/registar/", methods=("PUT", "POST",))
def regista_consulta_clinica(clinica):
    
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")
    
    error = ""
    ok_data_hora = 1
    
    if not paciente:
        error += "É necessário inserir um paciente. "
    if not is_decimal(paciente):
        error += "O paciente é identificado por um número décimal (ssn). "

    if not medico:
        error += "É necessário inserir um médico. "
    if not is_decimal(medico):
        error += "O médico é identificado por um número décimal (nif). "

    if not data:
        ok_data_hora = 0
        error += "É necessário inserir uma data. "
    if not is_date(data):
        ok_data_hora = 0
        error += "Data num formato inválido: YYYY-MM-DDq. "

    if not hora:
        ok_data_hora = 0
        error += "É necessário inserir uma hora. "
    if not is_time(hora):
        ok_data_hora = 0
        error += "Hora num formato inválido: HH:MM:SS. "

    if ok_data_hora:
        consulta_datetime = datetime.strptime(data + ' ' + hora, '%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
    
        if consulta_datetime < current_datetime:
            error += "Consulta não pode ser marcada, porque essa data é no passado. "

    if error != "":
        return jsonify({"message": error, "status": "erro"}), 404

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM clinica
                WHERE nome = %(clinica)s;
                """,
                {"clinica": clinica},
            )
                
            if not cur.fetchone():
                return jsonify({"message": "Clínica não existe.", "status": "404 NOT FOUND"}), 404
                
            cur.execute(
                """
                SELECT ssn
                FROM paciente
                WHERE ssn = %(paciente)s;
                """,
                {"paciente": paciente},
            )
            if not cur.fetchone():
                return jsonify({"message": "Paciente não existe.", "status": "404 NOT FOUND"}), 404
                
            cur.execute(
                """
                SELECT nif
                FROM medico
                WHERE nif = %(medico)s;
                """,
                {"medico": medico},
            )
            if not cur.fetchone():
                return jsonify({"message": "Médico não existe.", "status": "404 NOT FOUND"}), 404
            
            cur.execute(
                """
                SELECT *
                FROM consulta
                WHERE ssn = %(paciente)s AND data = %(data)s AND hora = %(hora)s;
                """,
                {"paciente": paciente,"data": data, "hora": hora},
            )
            if cur.fetchone():
                return jsonify({"message": "O paciente já tem uma marcação nesse horário.", "status": "erro"}), 404
                
            cur.execute(
                """
                SELECT *
                FROM consulta
                WHERE nif = %(medico)s AND data = %(data)s AND hora = %(hora)s;
                """,
                {"medico": medico,"data": data, "hora": hora},
            )
            if cur.fetchone():
                return jsonify({"message": "O medico já tem uma marcação nesse horário.", "status": "erro"}), 404
                
            cur.execute(
                """
                SELECT id
                FROM consulta
                ORDER BY id DESC
                LIMIT 1;
                """
            )
            id_curr = cur.fetchone()
            id = int(id_curr[0]) + 1

            cur.execute(
                """
                SELECT codigo_sns
                FROM consulta
                ORDER BY codigo_sns DESC
                LIMIT 1;
                """
            )
            codigo_sns_curr = cur.fetchone()
            codigo_sns = int(codigo_sns_curr[0]) + 1
            
            try:
                cur.execute(
                    """
                    INSERT INTO consulta (id, ssn, nif, nome, data, hora, codigo_sns)
                    VALUES(%(id)s, %(paciente)s, %(medico)s, %(clinica)s, %(data)s, %(hora)s, %(codigo_sns)s);
                    """,
                    {"id": id, "paciente": paciente, "medico": medico, "clinica": clinica, "data": data, "hora": hora, "codigo_sns": codigo_sns},
            )
                
            except psycopg.Error as e:
                if "ri_1" in str(e):
                    return jsonify({"message": "Hora inválida.", "status": "erro"}), 404
                elif "O médico não se pode consultar a si próprio." in str(e):
                    return jsonify({"message": "O médico não se pode consultar a si próprio.", "status": "erro"}), 404
                elif "Neste dia da semana o médico não dá consultas nesta clínica." in str(e):
                    return jsonify({"message": "Neste dia da semana o médico não dá consultas nesta clínica.", "status": "erro"}), 404

    return jsonify({"message": "Consulta registada com sucesso.", "status": "success"}), 200

@app.route("/a/<clinica>/cancelar/", methods=("DELETE", "POST",))
def cancela_consulta_clinica(clinica):
    
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")
    
    error = ""
    ok_data_hora = 1
    
    if not paciente:
        error += "É necessário inserir um paciente. "
    if not is_decimal(paciente):
        error += "O paciente é identificado por um número décimal (ssn). "

    if not medico:
        error += "É necessário inserir um médico. "
    if not is_decimal(medico):
        error += "O médico é identificado por um número décimal (nif). "

    if not data:
        ok_data_hora = 0
        error += "É necessário inserir uma data. "
    if not is_date(data):
        ok_data_hora = 0
        error += "Data num formato inválido: YYYY-MM-DDq. "

    if not hora:
        ok_data_hora = 0
        error += "É necessário inserir uma hora. "
    if not is_time(hora):
        ok_data_hora = 0
        error += "Hora num formato inválido: HH:MM:SS. "

    if ok_data_hora:
        consulta_datetime = datetime.strptime(data + ' ' + hora, '%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
    
        if consulta_datetime < current_datetime:
            error += "Consulta já foi realizada. "

    if error != "":
        return jsonify({"message": error, "status": "erro"}), 404

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM clinica
                WHERE nome = %(clinica)s;
                """,
                {"clinica": clinica},
            )
                
            if not cur.fetchone():
                return jsonify({"message": "Clínica não existe.", "status": "404 NOT FOUND"}), 404
                
            cur.execute(
                """
                SELECT ssn
                FROM paciente
                WHERE ssn = %(paciente)s;
                """,
                {"paciente": paciente},
            )
            if not cur.fetchone():
                return jsonify({"message": "Paciente não existe.", "status": "404 NOT FOUND"}), 404
                
            cur.execute(
                """
                SELECT nif
                FROM medico
                WHERE nif = %(medico)s;
                """,
                {"medico": medico},
            )
            if not cur.fetchone():
                return jsonify({"message": "Médico não existe.", "status": "404 NOT FOUND"}), 404
            
            cur.execute(
                """
                SELECT * FROM consulta
                WHERE ssn = %(paciente)s AND nif = %(medico)s AND data = %(data)s AND hora = %(hora)s;
                """,
                {"paciente": paciente, "medico": medico, "clinica": clinica, "data": data, "hora": hora},
            )
            if not cur.fetchone():
                return jsonify({"message": "Consulta não existe.", "status": "404 NOT FOUND"}), 404

            cur.execute(
                """
                DELETE FROM consulta
                WHERE ssn = %(paciente)s AND nif = %(medico)s AND data = %(data)s AND hora = %(hora)s;
                """,
                {"paciente": paciente, "medico": medico, "clinica": clinica, "data": data, "hora": hora},
            )
            
        return jsonify({"message": "Consulta cancelada com sucesso.", "status": "success"}), 200

if __name__ == "__main__":
    app.run()