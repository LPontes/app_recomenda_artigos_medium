import os.path
from flask import Flask
import os
import json
import run_backend 
import time

print(os.getcwd)
app = Flask(__name__)

def get_predictions():

    artigos = []
    
    artigos_novos_json = "novos_artigos.json"
    if not os.path.exists(artigos_novos_json):
        run_backend.update_db()
    
    last_update = os.path.getmtime(artigos_novos_json) * 1e9

    #if time.time_ns() - last_update > (720*3600*1e9): # aprox. 1 mes
    #    run_backend.update_db()

    with open("novos_artigos.json", 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
            artigos.append(line_json)

    predictions = []
    for artigo in artigos:
        predictions.append((artigo['link'], artigo['title'], float(artigo['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]

    predictions_formatted = []
    for e in predictions:
        #print(e)
        predictions_formatted.append("<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=e[1], link=e[0], score=str(e[2])))
  
    return '\n'.join(predictions_formatted), last_update

@app.route('/')
def main_page():
    preds, last_update = get_predictions()
    return """<head><h1>Recomendador de Artigos do Medium</h1></head>
    <body>
    Segundos desde a última atualização: {}
    <table>
             {}
    </table>
    </body>""".format((time.time_ns() - last_update) / 1e9, preds)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')