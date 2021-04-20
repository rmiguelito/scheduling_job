import json 
from operator import itemgetter
import re
import pprint
from datetime import datetime, timedelta
from flask import Flask, request

# Inciando o flask
app = Flask(__name__)

@app.route('/jobs', methods=['POST'])
def array_jobs():

    """
    Retorna um array de execução de jobs dentro de uma janela.
    Cada array tem o limite máximo de execução de 8 horas (padrão)
    """
    
    arquivo = "/home/miguel/vscode/scheduling_job/dados.json"
    dados = open(arquivo).read()
    dados_json = json.loads(dados)
    dados_ordenados = sorted(dados_json, key=itemgetter('Data Máxima de conclusão'))
    janela_inicio = request.json["Data Inicio"]
    janela_fim = request.json["Data Fim"]
    horas_bloco_intervalo = 8
    tempo_execucao = 0
    bloco = []
    resultado = []
    data_hora_previsto = datetime.strptime(janela_inicio, "%Y-%m-%d %H:%M:%S")

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
    return json.dumps(resultado)

if __name__ == '__main__':
    app.run(port=8080, debug=True)