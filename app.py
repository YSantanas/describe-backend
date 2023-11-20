from flask import Flask, request, jsonify
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/handle_data', methods=['POST'])
@cross_origin()
def handle_data():
 data = request.get_json()
 termino = data['termino']
 resultados = buscar_en_bing(termino)
 return jsonify({'results': resultados})

def buscar_en_bing(query, num_resultados=10):
 url = f"https://www.bing.com/search?q={query}&count={num_resultados}&setLang=es-MX&setmkt=es-MX   &setLang=es&mkt=es-MX"
 headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
 }

 response = requests.get(url, headers=headers)

 if response.status_code == 200:
     soup = BeautifulSoup(response.text, "html.parser")
     resultados = soup.find_all("li", class_="b_algo")

     resultados_list = []
     for idx, resultado in enumerate(resultados, start=1):
         titulo = resultado.find("h2").get_text()
         link = resultado.find("a")["href"]
         descripcion = resultado.find("p").get_text()
         
         resultados_list.append({
             'title': titulo,
             'url': link,
             'description': descripcion
         })
 else:
     print(f"Error al realizar la búsqueda. Código de estado: {response.status_code}")
     resultados_list = []

 return resultados_list


"""
    ===============================
    ========  I N G L E S =========
    ===============================    
"""


@app.route('/buscar_ing', methods=['POST'])
@cross_origin()
def buscar_ing():
 data = request.get_json()
 termino = data['termino']
 resultados = buscar_en_bing_ing(termino)
 return jsonify({'results': resultados})

def buscar_en_bing_ing(query, num_resultados=10):
 url = f"https://www.bing.com/search?q={query}&count={num_resultados}&setLang=en&mkt=en-US"
 headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
 }

 response = requests.get(url, headers=headers)

 if response.status_code == 200:
     soup = BeautifulSoup(response.text, "html.parser")
     resultados = soup.find_all("li", class_="b_algo")

     resultados_list2 = []
     for idx, resultado in enumerate(resultados, start=1):
         titulo = resultado.find("h2").get_text()
         link = resultado.find("a")["href"]
         descripcion = resultado.find("p").get_text()
         
         resultados_list2.append({
             'title': titulo,
             'url': link,
             'description': descripcion
         })
 else:
     print(f"Error al realizar la búsqueda. Código de estado: {response.status_code}")
     resultados_list2 = []

 return resultados_list2



if __name__ == "__main__":
  app.run(debug=True)
