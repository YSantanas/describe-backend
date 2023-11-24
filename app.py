from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
import re
import requests

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5500")


patrones_definiciones = [
    r"\.\s+(\w+)\b",
    r"\b(?:es\s+una)\b\s+(\w+)\b",
    r"\b(?:significa)\b\s+(\w+)\b",
    r"\b(?:se\s+define\s+como)\b\s+(\w+)\b",
    r"\b(?:se\s+refiere\s+a)\b\s+(\w+)\b",
    r"\b(?:corresponde\s+a)\b\s+(\w+)\b",
    r"\b(?:se\s+caracteriza\s+por)\b\s+(\w+)\b",
    r"\b(?:se\s+denomina)\b\s+(\w+)\b",
    r"\b(?:se\s+conoce\s+como)\b\s+(\w+)\b",
    r"\b(?:se\s+entiende\s+por)\b\s+(\w+)\b",
    r"\b(?:se\s+trata\s+de)\b\s+(\w+)\b",
]

patrones_casos = [
    r"\b(?:consiste\s+en)\b\s+(\w+)\b",
    r"\b(?:consta\s+de)\b\s+(\w+)\b",
    r"\b(?:está\s+compuesta\s+por)\b\s+(\w+)\b",
    r"\b(?:está\s+fabricada)\b\s+(\w+)\b",
    r"\b(?:tiene)\b\s+(\w+)\b",
    r"\b(?:se\s+encuentra\s+en)\b\s+(\w+)\b",
    r"\b(?:se\s+manifiesta\s+como)\b\s+(\w+)\b",
    r"\b(?:se\s+observa\s+en)\b\s+(\w+)\b",
    r"\b(?:se\s+produce\s+cuando)\b\s+(\w+)\b",
    r"\b(?:se\s+origina\s+por)\b\s+(\w+)\b",
]

patrones_funciones = [
    r"\b(?:se\s+usa)\b\s+(\w+)\b",
    r"\b(?:se\s+utiliza)\b\s+(\w+)\b",
    r"\b(?:sirve\s+para)\b\s+(\w+)\b",
    r"\b(?:cumple\s+la\s+función\s+de)\b\s+(\w+)\b",
    r"\b(?:apropiado\s+para)\b\s+(\w+)\b",
    r"\b(?:proporciona)\b\s+(\w+)\b",
    r"\b(?:favorece\s+la\s+)\b\s+(\w+)\b",
    r"\b(?:contribuye\s+a)\b\s+(\w+)\b",
    r"\b(?:mejora\s+)\b\s+(\w+)\b",
    r"\b(?:facilita\s+)\b\s+(\w+)\b",
]


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    termino = data["termino"]
    resultados_definiciones = buscar_en_bing(
        termino,
        patrones_definiciones,
    )
    resultados_casos = buscar_en_bing(
        termino,
        patrones_casos,
        #
    )
    resultados_funcion = buscar_en_bing(
        termino,
        patrones_funciones,
    )
    return jsonify(
        {
            "results_definiciones": resultados_definiciones,
            "results_casos": resultados_casos,
            "results_funcion": resultados_funcion,
        }
    )


# BUSCA LA DEFINICION DE LA PALABRA. Por ejemplo: "La computadora es una máquina que recibe y procesa datos para convertirlos en información útil."
def buscar_en_bing(
    query,
    patterns=[],
    blacklist=[],
    num_resultados=50,
):
    resultados_list = []

    for pagina in range(1, 6):
        offset = (pagina - 1) * num_resultados
        url = f"https://www.bing.com/search?q={query}&count={num_resultados}&setLang=es-ES&mkt=es-ES&first={offset}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                resultados = soup.find_all("li", class_="b_algo")
                resultados = list(dict.fromkeys(resultados))

                patron_definiciones = re.compile("|".join(patterns), re.IGNORECASE)

                for _, resultado in enumerate(resultados, start=1):
                    titulo = resultado.find("h2").get_text()
                    link = resultado.find("a")["href"]
                    descripcion = resultado.find("p").get_text()

                    if patron_definiciones.search(descripcion):
                        resultados_list.append(
                            {"title": titulo, "url": link, "description": descripcion}
                        )
            else:
                print(
                    f"Error al realizar la búsqueda. Código de estado: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")

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


@app.route("/buscar_ing", methods=["POST"])
@cross_origin()
def buscar_ing():
    data = request.get_json()
    termino = data["termino"]
    resultados = buscar_en_bing_ing(termino)
    return jsonify({"results": resultados})


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

            resultados_list2.append(
                {"title": titulo, "url": link, "description": descripcion}
            )
    else:
        print(
            f"Error al realizar la búsqueda. Código de estado: {response.status_code}"
        )
        resultados_list2 = []

    return resultados_list2


if __name__ == "__main__":
    app.run(debug=True)
