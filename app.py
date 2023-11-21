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

import re

# ... (código previo)

def buscar_en_bing(query, num_resultados=10):
    url = f"https://www.bing.com/search?q={query}&count={num_resultados}&setLang=es-MX&setmkt=es-MX&setLang=es&mkt=es-MX"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        resultados_definiciones = soup.find_all("li", class_="b_algo")
        patrones = [
            r'\b(definid[oa]s? como?)\b',
            r'\b(conocid[oa]s? como?)\b',
            r'\b(describ[ie]r?|descript[oa]s?)\b',
            r'\b(refiere? a)\b',
            r'\b(reconocid[oa]s? como?)\b',
            r'\b(es un[oa]s?|son)\b',
            r'\b(siendo|siendo un[oa]s?)\b',
            r'\b(apodad[oa]s?|apodado como?)\b',
            # ... otras variantes que puedan indicar definiciones
        ]


        patron_definiciones = re.compile('|'.join(patrones), re.IGNORECASE)

        resultados_list = []
        for idx, resultado in enumerate(resultados_definiciones, start=1):
            titulo = resultado.find("h2").get_text()
            link = resultado.find("a")["href"]
            descripcion = resultado.find("p").get_text()

            if patron_definiciones.search(descripcion):
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
OTRA FUNCION
"""

@app.route('/casos', methods=['POST'])
@cross_origin()
def casos():
    data = request.get_json()
    termino = data['termino']
    resultados = buscar_en_bing_casos(termino)
    return jsonify({'results2': resultados})

def buscar_en_bing_casos(query, num_resultados=100):
    url = f"https://www.bing.com/search?q={query}&count={num_resultados}&setLang=es-MX&setmkt=es-MX&setLang=es&mkt=es-MX"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        resultados_definiciones = soup.find_all("li", class_="b_algo")

        palabras_clave = [
        r'\b(cas[oa]s? de?)\b',
        r'\b(ejempl[oa]s? de?)\b',
        r'\b(instanci[ao]n[es]?)\b',
        r'\b(us[oa]s? de?)\b',
        r'\b(muestr[ao]s? de?)\b',
        r'\b(demostraci[óo]n[es]?)\b',
        r'\b(ilustraci[óo]n[es]?)\b',
        r'\b(exhibici[óo]n[es]?)\b',
        r'\b(modelo[os]? de?)\b',
        r'\b(representaci[óo]n[es]?)\b',
        r'\b(ejercicio[os]? de?)\b',
        r'\b(aplicaci[óo]n[es]?)\b',
        r'\b(instanciaci[óo]n[es]?)\b',
        r'\b(?:se utiliza[n]?|se emplea[n]?) para\b',
        r'\b(?:se utiliza[n]?|se emplea[n]?) como\b',
        r'\b(?:se usa[n]?|se emplea[n]?) para\b',
        r'\b(?:se usa[n]?|se emplea[n]?) como\b',
        r'\b(?:se usa[n]?|se emplea[n]?) en\b',
        r'\b(?:se usa[n]?|se emplea[n]?) con\b',
            # ... otras variantes que puedan indicar casos o ejemplos
        ]

        resultados_list = []
        for idx, resultado in enumerate(resultados_definiciones, start=1):
            titulo = resultado.find("h2").get_text()
            link = resultado.find("a")["href"]
            descripcion = resultado.find("p").get_text()

            if any(re.search(patron, descripcion, re.IGNORECASE) for patron in palabras_clave):
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
    ========  R E L A C I O N E S =========
    patrones_relacionados = [
    r'\b(relacionad[oa]s?)\b',
    r'\b(sobr[ea])\b',
    r'\b(acerca de)\b',
    r'\b(asociad[oa]s?)\b',
    r'\b(relativ[oa]s?)\b',
    r'\b(concernient[ea]s?)\b',
    r'\b(vinculad[oa]s?)\b',
    r'\b(referent[ea]s?)\b',
    r'\b(ligad[oa]s?)\b',
    r'\b(asocia[cd]([oa]s?) a)\b',
    r'\b(conectad[oa]s? con)\b',
    r'\b(involucrad[oa]s? en)\b',
    # ... otros patrones relacionados
]

    ===============================  
"""

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
