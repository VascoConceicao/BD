import random
import datetime
import sys

file = open('populate.sql', 'w')

NUMERO_CLINICAS = 5
NUMERO_MEDICOS = 60
NUMERO_MEDICOS_CLINICA_GERAL = 20
NUMERO_CONSULTAS_CLINICA_POR_DIA_MIN = 20
NUMERO_CONSULTAS_CLINICA_POR_DIA_MAX = 20
NUMERO_MIN_CONSULTAS_MEDICO_POR_DIA_MIN = 2
NUMERO_MIN_CONSULTAS_MEDICO_POR_DIA_MAX = 5

clinica_nomes = ['Clínica Vitalis', 'Clínica Bem-Estar', 'Clínica Renova', 'Clínica Equilíbrio', 'Clínica Vida Plena']
clinica_telefones = ['213123456', '218987654', '211456789', '215876543', '219345678']
clinica_moradas = ['Rua da Figueirinha 1, 2780-015 Oeiras', 'Avenida D. Francisco de Almeida 35, 2710-562 Sintra', 'Travessa do Prior 16, 2750-748 Cascais', 'Terreiro D. João V 28, 2640-492 Mafra', 'Avenida Tenente Valadim 16, 2560-274 Torres Vedras']

nome_proprios = ['Afonso', 'Ana', 'António', 'Beatriz', 'Bruno', 'Carla', 'Carlos', 'Catarina', 'Cristina', 'Daniel', 'Diana', 'Diogo', 'Eduardo', 'Ema', 'Fernando', 'Filipa', 'Filipe', 'Francisco', 'Gabriela', 'Gonçalo', 'Hugo', 'Inês', 'Isabel', 'Joana', 'João', 'José', 'Júlia', 'Laura', 'Leonor', 'Luis', 'Luísa', 'Manuel', 'Margarida', 'Mariana', 'Mário', 'Marta', 'Miguel', 'Nuno', 'Patrícia', 'Paulo', 'Pedro', 'Rita', 'Rui', 'Sandra', 'Sara', 'Sérgio', 'Sofia', 'Susana', 'Tiago', 'Tomás', 'Vasco', 'Vera', 'Vítor', 'Henrique', 'Adriana', 'Alberto', 'Alexandra', 'Alexandre', 'Alice', 'Amélia', 'André', 'Ângela', 'Aníbal', 'Antónia', 'Armando', 'Bárbara', 'Bernardo', 'Camila', 'Carolina', 'Cátia', 'Cecília', 'Cláudia', 'Cheila', 'Célia', 'Dário', 'David', 'Domingos', 'Duarte', 'Elsa', 'Elvira', 'Emília', 'Estela', 'Eugénio', 'Eulália', 'Fábio', 'Fabrício', 'Fernanda', 'Fernandina', 'Fernando', 'Flávia', 'Florinda', 'Frederico', 'Gisela']
nome_apelidos = ['Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Jesus', 'Sousa', 'Fernandes', 'Gomes', 'Lopes', 'Marques', 'Almeida', 'Alves', 'Ribeiro', 'Carvalho', 'Teixeira', 'Moreira', 'Correia', 'Barbosa', 'Pinto', 'Mendes', 'Soares', 'Cardoso', 'Nunes', 'Simões', 'Machado', 'Miranda', 'Cruz', 'Cunha', 'Batista', 'Neves', 'Araújo', 'Henriques', 'Reis', 'Rocha', 'Vieira', 'Monteiro', 'Santana', 'Figueiredo', 'Matos', 'Dias', 'Correia', 'Fonseca', 'Azevedo', 'Freitas', 'Leal', 'Pinheiro', 'Garcia', 'Guerreiro', 'Ramos', 'Borges', 'Tavares', 'Magalhães', 'Melo', 'Vargas', 'Ramos', 'Vieira', 'Albuquerque', 'Vaz', 'Faria', 'Aguiar', 'Brito', 'Caldeira', 'Antunes', 'Câmara', 'Carmo', 'Castro', 'Coelho', 'Conceição', 'Esteves', 'Faria', 'Galvão', 'Gama', 'Leite', 'Marinho', 'Nóbrega', 'Novais', 'Oliveira', 'Pascoal', 'Queirós', 'Quintana', 'Sampaio', 'Silveira', 'Valente', 'Ventura', 'Xavier', 'Zagalo', 'Luz', 'Zeferino']

morada_ruas = ['Rua', 'Avenida', 'Travessa', 'Praceta', 'Praça', 'Beco', 'Vale', 'Quinta', 'Ruela', 'Estrada', 'Largo', 'Alameda']
morada_nomes = ['Flor', 'Rosa', 'Violeta', 'Magnólia', 'Tulipa', 'Bolacha', 'Caneta', 'Livro', 'Caderno', 'Limão']
morada_adjetivos = ['Alegre', 'Gentil', 'Veloz', 'Capaz', 'Radical', 'Leal', 'Feliz', 'Grande', 'Legal', 'Simples']
morada_localidades = ['Almeida', 'Almodôvar', 'Alter do Chão', 'Alvito', 'Cruz de Pau', 'Avis', 'Barrancos', 'Castro Verde', 'Castro Marim', 'Crato', 'Ferreira do Alentejo', 'Freixo de Espada à Cinta', 'Mação', 'Mértola', 'Monchique', 'Montalegre', 'Mourão', 'Odemira', 'Penamacor', 'Beja', 'Portel', 'Porto de Mós', 'Sernancelhe', 'Tabuaço', 'Vila Nova de Cerveira', 'Vila Velha de Ródão', 'Funchal']

especialidades = ['Ortopedia', 'Cardiologia', 'Pediatria', 'Pneumologia', 'Endocrinologia']

medicamento_nomes = ['Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Diazepam', 'Omeprazol', 'Ciprofloxacina', 'Atorvastatina', 'Metformina', 'Losartan', 'Furosemida', 'Escitalopram', 'Codeína', 'Ranitidina', 'Loratadina', 'Dexametasona', 'Fenitoína', 'Pregabalina', 'Tramadol', 'Enalapril', 'Cetirizina', 'Insulina', 'Morfina', 'Fluoxetina', 'Cefalexina', 'Metotrexato', 'Levotiroxina', 'Captopril', 'Diclofenaco', 'Sinvastatina', 'Clonazepam', 'Risperidona', 'Fentanil', 'Gabapentina', 'Lisinopril', 'Mirtazapina', 'Carbamazepina', 'Olanzapina', 'Sertralina', 'Digoxina', 'Budesonida', 'Bupropiona', 'Amitriptilina', 'Pantoprazol', 'Warfarina', 'Tolbutamida', 'Rivotril', 'Lamotrigina', 'Quetiapina']

parametro_sem_valor_nomes = ['Dor de cabeça', 'Náusea', 'Vómito', 'Tontura', 'Fadiga', 'Dor abdominal', 'Tosse', 'Dor no peito', 'Palpitações', 'Falta de ar', 'Diarreia', 'Prisão de ventre', 'Ardência ao urinar', 'Sangramento', 'Comichão', 'Erupção cutânea', 'Inchaço', 'Dor nas articulações', 'Rigidez muscular', 'Dormência', 'Formigueiro', 'Fraqueza muscular', 'Perda de apetite', 'Calafrios', 'Sensibilidade à luz', 'Olhos vermelhos', 'Visão turva', 'Zumbido nos ouvidos', 'Perda de audição', 'Dificuldade para engolir', 'Rouquidão', 'Gânglios linfáticos inchados', 'Perda de peso inexplicada', 'Boca seca', 'Sede excessiva', 'Urinar com frequência', 'Dor lombar', 'Espasmos musculares', 'Desmaios', 'Confusão mental', 'Perda de memória', 'Mudança de humor', 'Insónia', 'Sonolência excessiva', 'Pesadelos', 'Olhos secos', 'Pálpebras inchadas', 'Sangramento nasal', 'Congestão nasal', 'Dor de garganta']

parametro_com_valor_nomes = ['Pressão arterial sistólica', 'Pressão arterial diastólica', 'Frequência cardíaca', 'Temperatura corporal', 'IMC', 'Glicemia em jejum', 'Nível de hemoglobina', 'Nível de hematocrito', 'Contagem de glóbulos brancos', 'Contagem de glóbulos vermelhos', 'Nível de plaquetas', 'Nível de colesterol total', 'Nível de colesterol LDL', 'Nível de colesterol HDL', 'Nível de triglicérides', 'Nível de ácido úrico', 'Nível de creatinina', 'Taxa de filtração glomerular', 'Nível de sódio', 'Nível de potássio']
parametro_com_valor_dominios = [[90, 120], [60, 80], [60, 100], [36.1, 37.2], [18.5, 24.9], [70, 100], [12, 16], [36, 46], [4_500, 11_000], [4.2, 5.4], [150_000, 450_000], [0, 200], [0, 100], [40, 50], [0, 150], [3.5, 7.2], [0.5, 1.1], [90, 1000], [135, 145], [3.5, 5.0]]

print('0/1 - Inserindo clínicas...\n')

clinica_inicio = True

clinicas = []
for i in range(NUMERO_CLINICAS):
    clinica_nome = clinica_nomes[i]
    clinica_telefone = clinica_telefones[i]
    clinica_morada = clinica_moradas[i]
    clinicas += [[clinica_nome, clinica_telefone, clinica_morada]]
    if clinica_inicio:
        file.write(f'INSERT INTO clinica VALUES (\'{clinica_nome}\', \'{clinica_telefone}\', \'{clinica_morada}\')')
        clinica_inicio = False
    else:
        file.write(f', (\'{clinica_nome}\', \'{clinica_telefone}\', \'{clinica_morada}\')')

file.write(';\n')

print('1/1 - Inseridas todos as clínicas.\n')

print('0/1 - Inserindo enfermeiros...\n')

enfermeiro_inicio = True

enfermeiro_nifs_nomes = {}
for clinica_nome in clinica_nomes:
    for i in range(random.randint(5, 6)):
        enfermeiro_nif = random.randint(100000000, 999999999)
        enfermeiro_nome = nome_proprios[random.randint(0, len(nome_proprios) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)]
        enfermeiro_telefone = random.randint(960000000, 969999999)
        enfermeiro_morada = morada_ruas[random.randint(0, len(morada_ruas) - 1)] + ' ' + morada_nomes[random.randint(0, len(morada_nomes) - 1)] + ' ' + morada_adjetivos[random.randint(0, len(morada_adjetivos) - 1)] + ' ' + str(random.randint(1, 99)) + ', ' + str(random.randint(1000, 9999)) + '-' + str(random.randint(100, 999)) + ' ' + morada_localidades[random.randint(0, len(morada_localidades) - 1)]
        enfermeiro_clinica = clinica_nome
        while enfermeiro_nif in enfermeiro_nifs_nomes.keys():
            enfermeiro_nif = random.randint(100000000, 999999999)
        while enfermeiro_nome in enfermeiro_nifs_nomes.values():
            enfermeiro_nome = nome_proprios[random.randint(0, len(nome_proprios) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)]
        enfermeiro_nifs_nomes[enfermeiro_nif] = enfermeiro_nome
        if enfermeiro_inicio:
            file.write(f'INSERT INTO enfermeiro VALUES (\'{enfermeiro_nif}\', \'{enfermeiro_nome}\', \'{enfermeiro_telefone}\', \'{enfermeiro_morada}\', \'{enfermeiro_clinica}\')')
            enfermeiro_inicio = False
        else:
            file.write(f', (\'{enfermeiro_nif}\', \'{enfermeiro_nome}\', \'{enfermeiro_telefone}\', \'{enfermeiro_morada}\', \'{enfermeiro_clinica}\')')

file.write(';\n')

print('1/1 - Inseridos todos os enfermeiros.\n')

print('0/1 - Inserindo médicos...\n')

medico_inicio = True

medico_nifs_nomes = {}
for i in range(60):
    medico_nif = random.randint(100000000, 999999999)
    medico_nome = nome_proprios[random.randint(0, len(nome_proprios) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)]
    medico_telefone = random.randint(960000000, 969999999)
    medico_morada = morada_ruas[random.randint(0, len(morada_ruas) - 1)] + ' ' + morada_nomes[random.randint(0, len(morada_nomes) - 1)] + ' ' + morada_adjetivos[random.randint(0, len(morada_adjetivos) - 1)] + ' ' + str(random.randint(1, 99)) + ', ' + str(random.randint(1000, 9999)) + '-' + str(random.randint(100, 999)) + ' ' + morada_localidades[random.randint(0, len(morada_localidades) - 1)]
    if i < NUMERO_MEDICOS_CLINICA_GERAL:
        medico_especialidade = 'Clínica Geral'
    elif i == NUMERO_MEDICOS_CLINICA_GERAL + 1:
        medico_especialidade = 'Ortopedia'
    elif i == NUMERO_MEDICOS_CLINICA_GERAL + 1:
        medico_especialidade = 'Cardiologia'
    else:
        medico_especialidade = especialidades[random.randint(0, len(especialidades) - 1)]
    while medico_nif in medico_nifs_nomes.keys() or medico_nif in enfermeiro_nifs_nomes.keys():
        medico_nif = random.randint(100000000, 999999999)
    while medico_nome in medico_nifs_nomes.values():
        medico_nome = nome_proprios[random.randint(0, len(nome_proprios) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)]
    medico_nifs_nomes[medico_nif] = medico_nome
    if medico_inicio:
        file.write(f'INSERT INTO medico VALUES (\'{medico_nif}\', \'{medico_nome}\', \'{medico_telefone}\', \'{medico_morada}\', \'{medico_especialidade}\')')
        medico_inicio = False
    else:
        file.write(f', (\'{medico_nif}\', \'{medico_nome}\', \'{medico_telefone}\', \'{medico_morada}\', \'{medico_especialidade}\')')

file.write(';\n')

print('1/1 - Inseridos todos os médicos.\n')

print('0/1 - Inserindo relações de trabalho...\n')

trabalho_inicio = True

alocacao = []
for i in range(NUMERO_CLINICAS):
    alocacao_clinica = []
    for dia_da_semana in range(7):
        alocacao_dia = []
        for k in range(8):
            medico_nif = list(medico_nifs_nomes.keys())[random.randint(0, len(medico_nifs_nomes.keys()) - 1)]
            ok = False
            while not ok:
                ok = True
                medico_nif = list(medico_nifs_nomes)[random.randint(0, len(medico_nifs_nomes.keys()) - 1)]
                if medico_nif in alocacao_dia:
                    ok = False
                for l in range(i):
                    if medico_nif in alocacao[l][dia_da_semana]:
                        ok = False
            alocacao_dia += [medico_nif]
        alocacao_clinica += [alocacao_dia]
    alocacao += [alocacao_clinica]

for i in range(NUMERO_MEDICOS):
    clinicas_no = 0
    dia_da_semana_clinica = {}
    for j in range(len(alocacao)):
        for k in range(len(alocacao[j])):
            for medico_nif in alocacao[j][k]:
                if medico_nif == list(medico_nifs_nomes.keys())[i]:
                    dia_da_semana_clinica[k] = j
                    if j not in clinicas:
                        clinicas_no += 1
    while len(set(dia_da_semana_clinica.values())) < 2:
        clinica_index = random.randint(0, NUMERO_CLINICAS - 1)
        dia_da_semana = random.randint(0, 6)
        while dia_da_semana in dia_da_semana_clinica.keys() or clinica_index in dia_da_semana_clinica.values():
            clinica_index = random.randint(0, len(clinica_nomes) - 1)
            dia_da_semana = random.randint(0, 6)
        alocacao[clinica_index][dia_da_semana] += [list(medico_nifs_nomes.keys())[i]]
        dia_da_semana_clinica[dia_da_semana] = clinica_index

for clinica_index in range(len(alocacao)):
    for dia_da_semana in range(len(alocacao[clinica_index])):
        for nif_medico in alocacao[clinica_index][dia_da_semana]:
            if trabalho_inicio:
                file.write(f'INSERT INTO trabalha VALUES (\'{nif_medico}\', \'{clinica_nomes[clinica_index]}\', {dia_da_semana})')
                trabalho_inicio = False
            else:
                file.write(f', (\'{nif_medico}\', \'{clinica_nomes[clinica_index]}\', {dia_da_semana})')

file.write(';\n')

print('1/1 - Inseridas todas as relações de trabalho.\n')

print('0/1 - Inserindo pacientes...\n')

paciente_inicio = True

paciente_ssns_nifs = {}
for i in range(random.randint(5000, 5500)):
    paciente_ssn = random.randint(10000000000, 99999999999)
    paciente_nif = random.randint(100000000, 999999999)
    paciente_nome = nome_proprios[random.randint(0, len(nome_proprios) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)] + ' ' + nome_apelidos[random.randint(0, len(nome_apelidos) - 1)]
    paciente_telefone = random.randint(960000000, 969999999)
    paciente_morada = morada_ruas[random.randint(0, len(morada_ruas) - 1)] + ' ' + morada_nomes[random.randint(0, len(morada_nomes) - 1)] + ' ' + morada_adjetivos[random.randint(0, len(morada_adjetivos) - 1)] + ' ' + str(random.randint(1, 99)) + ', ' + str(random.randint(1000, 9999)) + '-' + str(random.randint(100, 999)) + ' ' + morada_localidades[random.randint(0, len(morada_localidades) - 1)]
    paciente_data_nascimento = str(random.randint(1940, 2023)) + '-' + '{:02d}'.format(random.randint(1, 12)) + '-' + '{:02d}'.format(random.randint(1, 28))
    while paciente_ssn in paciente_ssns_nifs.keys():
        paciente_ssn = random.randint(10000000000, 99999999999)
    while paciente_nif in paciente_ssns_nifs.values():
        paciente_nif = random.randint(100000000, 999999999)
    if paciente_nif in enfermeiro_nifs_nomes.keys():
        paciente_nome = enfermeiro_nifs_nomes[paciente_nif]
    elif paciente_nif in medico_nifs_nomes.keys():
        paciente_nome = medico_nifs_nomes[paciente_nif]
    paciente_ssns_nifs[paciente_ssn] = paciente_nif
    if paciente_inicio:
        file.write(f'INSERT INTO paciente VALUES (\'{paciente_ssn}\', \'{paciente_nif}\', \'{paciente_nome}\', \'{paciente_telefone}\', \'{paciente_morada}\', \'{paciente_data_nascimento}\')')
        paciente_inicio = False
    else:
        file.write(f', (\'{paciente_ssn}\', \'{paciente_nif}\', \'{paciente_nome}\', \'{paciente_telefone}\', \'{paciente_morada}\', \'{paciente_data_nascimento}\')')

file.write(';\n')

print('1/1 - Inseridos todos os pacientes.\n')

print('0/1 - Inserindo consultas...\n')

consulta_inicio = True

consulta_medicos_data_hora = {}
consulta_codigos_sns_data_hora = {}
consulta_ids_data_hora = {}
for medico_nif in medico_nifs_nomes.keys():
    consulta_medicos_data_hora[medico_nif] = []
consulta_pacientes_data_hora = {}
for paciente_ssn in paciente_ssns_nifs.keys():
    consulta_pacientes_data_hora[paciente_ssn] = []
consulta_id = 0
consulta_codigo_sns = 100000000000
for ano in [2023, 2024]:
    for mes in range(1, 13):
        for dia in range(1, 32):
            try:
                date = datetime.date(ano, mes, dia)
            except ValueError:
                continue
            dia_da_semana = date.weekday() + 1
            if dia_da_semana == 7:
                dia_da_semana = 0
            for clinica_index in range(NUMERO_CLINICAS):
                for i in range(random.randint(NUMERO_CONSULTAS_CLINICA_POR_DIA_MIN, NUMERO_CONSULTAS_CLINICA_POR_DIA_MAX)):
                    consulta_ssn = list(paciente_ssns_nifs.keys())[random.randint(0, len(paciente_ssns_nifs.keys()) - 1)]
                    consulta_nif = alocacao[clinica_index][dia_da_semana][random.randint(0, len(alocacao[clinica_index][dia_da_semana]) - 1)]
                    consulta_nome = clinica_nomes[clinica_index]
                    horas = random.randint(8, 17)
                    if horas > 12:
                        horas += 1
                    minutos = 30 * random.randint(0, 1)
                    segundos = 0
                    consulta_hora = '{:02d}'.format(horas) + ':' + '{:02d}'.format(minutos) + ':' + '{:02d}'.format(segundos)
                    while [date, consulta_hora] in consulta_pacientes_data_hora[consulta_ssn] or [date, consulta_hora] in consulta_medicos_data_hora[consulta_nif]:
                        horas = random.randint(8, 17)
                        if horas > 12:
                            horas += 1
                        minutos = 30 * random.randint(0, 1)
                        segundos = 0
                        consulta_hora = '{:02d}'.format(horas) + ':' + '{:02d}'.format(minutos) + ':' + '{:02d}'.format(segundos)
                    consulta_data = str(date)
                    consulta_codigos_sns_data_hora[consulta_codigo_sns] = [consulta_data, consulta_hora]
                    consulta_ids_data_hora[consulta_id] = [consulta_data, consulta_hora]
                    if consulta_inicio:
                        file.write(f'INSERT INTO consulta VALUES (\'{consulta_id}\', \'{consulta_ssn}\', \'{consulta_nif}\', \'{consulta_nome}\', \'{consulta_data}\', \'{consulta_hora}\', \'{consulta_codigo_sns}\')')
                        consulta_inicio = False
                    else:
                        file.write(f', (\'{consulta_id}\', \'{consulta_ssn}\', \'{consulta_nif}\', \'{consulta_nome}\', \'{consulta_data}\', \'{consulta_hora}\', \'{consulta_codigo_sns}\')')
                    consulta_id += 1
                    consulta_codigo_sns += 1
                    consulta_pacientes_data_hora[consulta_ssn] += [[date, consulta_hora]]
                    consulta_medicos_data_hora[consulta_nif] += [[date, consulta_hora]]

print('1/3 - Inseridas pelo menos 20 consultas por dia em todas as clínicas.\n')

for consulta_ssn in paciente_ssns_nifs.keys():
    while len(consulta_pacientes_data_hora[consulta_ssn]) < 1:
        date = datetime.date(2023, 1, 1) + datetime.timedelta(random.randint(0, 365 * 2))
        dia_da_semana = date.weekday() + 1
        if dia_da_semana == 7:
            dia_da_semana = 0
        clinica_index = random.randint(0, 4)
        consulta_nif = alocacao[clinica_index][dia_da_semana][random.randint(0, len(alocacao[clinica_index][dia_da_semana]) - 1)]
        consulta_nome = clinica_nomes[clinica_index]
        horas = random.randint(8, 17)
        if horas > 12:
            horas += 1
        minutos = 30 * random.randint(0, 1)
        segundos = 0
        consulta_hora = '{:02d}'.format(horas) + ':' + '{:02d}'.format(minutos) + ':' + '{:02d}'.format(segundos)
        while [date, consulta_hora] in consulta_pacientes_data_hora[consulta_ssn] or [date, consulta_hora] in consulta_medicos_data_hora[consulta_nif]:
            date = datetime.date(2023, 1, 1) + datetime.timedelta(random.randint(0, 365 * 2))
            dia_da_semana = date.weekday() + 1
            if dia_da_semana == 7:
                dia_da_semana = 0
            clinica_index = random.randint(0, 4)
            consulta_nif = alocacao[clinica_index][dia_da_semana][random.randint(0, len(alocacao[clinica_index][dia_da_semana]) - 1)]
            horas = random.randint(8, 17)
            if horas > 12:
                horas += 1
            minutos = 30 * random.randint(0, 1)
            segundos = 0
            consulta_hora = '{:02d}'.format(horas) + ':' + '{:02d}'.format(minutos) + ':' + '{:02d}'.format(segundos)
        consulta_data = str(date)
        consulta_codigos_sns_data_hora[consulta_codigo_sns] = [consulta_data, consulta_hora]
        consulta_ids_data_hora[consulta_id] = [consulta_data, consulta_hora]
        file.write(f', (\'{consulta_id}\', \'{consulta_ssn}\', \'{consulta_nif}\', \'{consulta_nome}\', \'{consulta_data}\', \'{consulta_hora}\', \'{consulta_codigo_sns}\')')
        consulta_id += 1
        consulta_codigo_sns += 1
        consulta_medicos_data_hora[consulta_nif] += [[date, consulta_hora]]
        consulta_pacientes_data_hora[consulta_ssn] += [[date, consulta_hora]]

print('2/3 - Inserida pelo menos 1 consulta em todos os pacientes.\n')

date = datetime.date(2023, 1, 1)
while date.year < 2025:
    dia_da_semana = date.weekday() + 1
    if dia_da_semana == 7:
        dia_da_semana = 0
    for clinica_index in range(NUMERO_CLINICAS):
        for consulta_nif in alocacao[clinica_index][dia_da_semana]:
            i = 0
            for [data, hora] in consulta_medicos_data_hora[consulta_nif]:
                if data == date:
                    i += 1
            lim = random.randint(NUMERO_MIN_CONSULTAS_MEDICO_POR_DIA_MIN, NUMERO_MIN_CONSULTAS_MEDICO_POR_DIA_MAX)
            while i < lim:
                consulta_ssn = list(paciente_ssns_nifs.keys())[random.randint(0, len(paciente_ssns_nifs.keys()) - 1)]
                consulta_nome = clinica_nomes[clinica_index]
                horas = random.randint(8, 17)
                if horas > 12:
                    horas += 1
                minutos = 30 * random.randint(0, 1)
                segundos = 0
                consulta_hora = '{:02d}'.format(horas) + ':' + '{:02d}'.format(minutos) + ':' + '{:02d}'.format(segundos)
                while [date, consulta_hora] in consulta_pacientes_data_hora[consulta_ssn] or [date, consulta_hora] in consulta_medicos_data_hora[consulta_nif]:
                    consulta_ssn = list(paciente_ssns_nifs.keys())[random.randint(0, len(paciente_ssns_nifs.keys()) - 1)]
                    horas = random.randint(8, 17)
                    if horas > 12:
                        horas += 1
                    minutos = 30 * random.randint(0, 1)
                    segundos = 0
                    consulta_hora = '{:02d}'.format(horas) + ':' + '{:02d}'.format(minutos) + ':' + '{:02d}'.format(segundos)
                consulta_data = str(date)
                consulta_codigos_sns_data_hora[consulta_codigo_sns] = [consulta_data, consulta_hora]
                consulta_ids_data_hora[consulta_id] = [consulta_data, consulta_hora]
                consulta_medicos_data_hora[consulta_nif] += [[date, consulta_hora]]
                consulta_pacientes_data_hora[consulta_ssn] += [[date, consulta_hora]]
                file.write(f', (\'{consulta_id}\', \'{consulta_ssn}\', \'{consulta_nif}\', \'{consulta_nome}\', \'{consulta_data}\', \'{consulta_hora}\', \'{consulta_codigo_sns}\')')
                consulta_id += 1
                consulta_codigo_sns += 1
                i = 0
                for [data, hora] in consulta_medicos_data_hora[consulta_nif]:
                    if data == date:
                        i += 1
    date = date + datetime.timedelta(1)

file.write(';\n')

print('3/3 - Inseridas pelo menos 2 consultas por dia em todos os médicos que trabalham nesse dia.\n')

print('0/1 - Inserindo receitas...\n')

receita_inicio = True

for receita_codigo_sns in consulta_codigos_sns_data_hora.keys():
    data, hora = consulta_codigos_sns_data_hora[receita_codigo_sns]
    if datetime.datetime.strptime(data + ' ' + hora, '%Y-%m-%d %H:%M:%S') < datetime.datetime.now() and random.random() < 0.8:
        medicamentos_no = random.randint(1, 6)
        medicamentos = []
        for i in range(medicamentos_no):
            receita_medicamento = medicamento_nomes[random.randint(0, len(medicamento_nomes) - 1)]
            while receita_medicamento in medicamentos:
                receita_medicamento = medicamento_nomes[random.randint(0, len(medicamento_nomes) - 1)]
            medicamentos += [receita_medicamento]
            receita_quantidade = random.randint(1, 3)
            if receita_inicio:
                file.write(f'INSERT INTO receita VALUES (\'{receita_codigo_sns}\', \'{receita_medicamento}\', \'{receita_quantidade}\')')
                receita_inicio = False
            else:
                file.write(f', (\'{receita_codigo_sns}\', \'{receita_medicamento}\', \'{receita_quantidade}\')')

file.write(';\n')

print('1/1 - Inseridas todas as receitas.\n')

print('0/1 - Inserindo observações...\n')

observacao_sem_valor_inicio = True
linha_sem_valor = ''
observacao_com_valor_inicio = True
linha_com_valor = ''
for observacao_id in consulta_ids_data_hora.keys():
    data, hora = consulta_ids_data_hora[observacao_id]
    if datetime.datetime.strptime(data + ' ' + hora, '%Y-%m-%d %H:%M:%S') < datetime.datetime.now():
        parametros_sem_valor_no = random.randint(1, 5)
        parametros_sem_valor = []
        for i in range(parametros_sem_valor_no):
            observacao_parametro = parametro_sem_valor_nomes[random.randint(0, len(parametro_sem_valor_nomes) - 1)]
            while observacao_parametro in parametros_sem_valor:
                observacao_parametro = parametro_sem_valor_nomes[random.randint(0, len(parametro_sem_valor_nomes) - 1)]
            parametros_sem_valor += [observacao_parametro]
            if observacao_sem_valor_inicio:
                linha_sem_valor += f'INSERT INTO observacao VALUES (\'{observacao_id}\', \'{observacao_parametro}\')'
                observacao_sem_valor_inicio = False
            else:
                linha_sem_valor += f', (\'{observacao_id}\', \'{observacao_parametro}\')'
        parametros_com_valor_no = random.randint(0, 3)
        parametros_com_valor = []
        for i in range(parametros_com_valor_no):
            j = random.randint(0, len(parametro_com_valor_nomes) - 1)
            observacao_parametro = parametro_com_valor_nomes[j]
            while observacao_parametro in parametros_com_valor:
                j = random.randint(0, len(parametro_com_valor_nomes) - 1)
                observacao_parametro = parametro_com_valor_nomes[j]
            parametros_com_valor += [observacao_parametro]
            observacao_valor = random.uniform(parametro_com_valor_dominios[j][0], parametro_com_valor_dominios[j][1])
            if observacao_com_valor_inicio:
                linha_com_valor += f'INSERT INTO observacao VALUES (\'{observacao_id}\', \'{observacao_parametro}\', {observacao_valor})'
                observacao_com_valor_inicio = False
            else:
                linha_com_valor += f', (\'{observacao_id}\', \'{observacao_parametro}\', {observacao_valor})'

linha_sem_valor += ';\n'
linha_com_valor += ';\n'

file.write(linha_sem_valor)
file.write(linha_com_valor)

print('1/1 - Inseridas todas as observações.\n')

file.close()

