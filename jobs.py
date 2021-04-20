import json
from operator import itemgetter
import pprint

arquivo = "/home/miguel/vscode/scheduling_job/dados.json"
dados = open(arquivo).read()
dados_json = json.loads(dados)
dados_ordenados = sorted(dados_json, key=itemgetter("Data Máxima de conclusão"))

pprint.pprint(dados_ordenados, indent=2)