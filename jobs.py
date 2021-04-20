import json
from operator import itemgetter
import pprint
from datetime import datetime, timedelta
import re

arquivo = "/home/miguel/vscode/scheduling_job/dados.json"
dados = open(arquivo).read()
dados_json = json.loads(dados)
dados_ordenados = sorted(dados_json, key=itemgetter("Data Máxima de conclusão"))
#pprint.pprint(dados_ordenados, indent=2)
janela_inicio = "2019-11-10 09:00:00"
janela_fim = "2019-11-11 12:00:00"
data_hora_previsto = datetime.strptime(janela_inicio, "%Y-%m-%d %H:%M:%S")
tempo_execucao = 0
horas_bloco_intervalo = 8
bloco = []
resultado = []

#import pdb ; pdb.set_trace()
for job in dados_ordenados:
    if janela_inicio <= job["Data Máxima de conclusão"] <= janela_fim:
        tempo = re.match("^[0-9]+", job["Tempo estimado"])
        tempo_estimado = int(tempo.group(0))
        #print(tempo_estimado, job["ID"])
        if tempo_estimado <= horas_bloco_intervalo and \
            data_hora_previsto + timedelta(hours=tempo_estimado) <= datetime.strptime(job["Data Máxima de conclusão"], "%Y-%m-%d %H:%M:%S"):
            data_hora_previsto = data_hora_previsto + timedelta(hours=tempo_estimado)
            #print(job["ID"], data_hora_previsto)
            if (tempo_execucao + tempo_estimado) <= horas_bloco_intervalo:
                tempo_execucao = tempo_execucao + tempo_estimado
                bloco.append(job["ID"])
            else:
                resultado.append(bloco)
                bloco = []
                tempo_execucao = tempo_estimado
                bloco.append(job["ID"])
resultado.append(bloco)
print(json.dumps(resultado))