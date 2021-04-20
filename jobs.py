import json
from operator import itemgetter
import pprint
from datetime import datetime, timedelta
import re

def array_jobs(arquivo, janela_inicio, janela_fim, horas_bloco_intervalo=8):
    """
    Retorna um array de execução de jobs dentro de uma janela.
    Cada array tem o limite máximo de execução de 8 horas (padrão)
    >>> array_jobs("dados.json", "2019-11-10 09:00:00", "2019-11-11 12:00:00")
    [[1, 3], [2]]
    """

    #arquivo = "/home/miguel/vscode/scheduling_job/dados.json"
    dados = open(arquivo).read()
    dados_json = json.loads(dados)
    # Lendo e ordenando o json da massa
    dados_ordenados = sorted(dados_json, key=itemgetter("Data Máxima de conclusão"))
    janela_inicio = "2019-11-10 09:00:00"
    janela_fim = "2019-11-11 12:00:00"
    data_hora_previsto = datetime.strptime(janela_inicio, "%Y-%m-%d %H:%M:%S")
    tempo_execucao = 0
    horas_bloco_intervalo = 8
    bloco = []
    resultado = []

 # Loop para validar os dados e criar o array
    for job in dados_ordenados:
         # Validando se o job está dentro da janela de execução    
        if janela_inicio <= job["Data Máxima de conclusão"] <= janela_fim:
            tempo = re.match("^[0-9]+", job["Tempo estimado"])
            tempo_estimado = int(tempo.group(0))
            # Validando se o tempo_estimado do job está dentro do bloco de intervalo e respeitando a data máxima do job
            if tempo_estimado <= horas_bloco_intervalo and \
                data_hora_previsto + timedelta(hours=tempo_estimado) <= datetime.strptime(job["Data Máxima de conclusão"], "%Y-%m-%d %H:%M:%S"):
                data_hora_previsto = data_hora_previsto + timedelta(hours=tempo_estimado)
                if (tempo_execucao + tempo_estimado) <= horas_bloco_intervalo:
                    tempo_execucao = tempo_execucao + tempo_estimado
                    bloco.append(job["ID"]) # Incrementando o ID no bloco
                else:
                    resultado.append(bloco)
                    bloco = []
                    tempo_execucao = tempo_estimado
                    bloco.append(job["ID"])                
    resultado.append(bloco) # Incrementando o bloco para o resultado
    print(json.dumps(resultado))

import doctest
import sys
doctest.testmod()