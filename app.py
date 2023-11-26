import spacy
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from palabras_clave import (
    palabras_clave_definicion,
    palabras_clave_componentes,
    palabras_clave_funcionalidades,
    palabras_clave_definicion2,
    palabras_clave_componentes2,
    palabras_clave_funcionalidades2,
)

app = Flask(__name__)
CORS(app)


@app.route("/buscar", methods=["POST"])
def buscar():
    palabra = request.get_json()["palabra"]
    print(f"Palabra: {palabra}")

    # Realiza búsqueda en Bing como ejemplo
    print("Buscando en Bing...")
    resultados = buscar_bing(palabra)

    # Filtra resultados
    definiciones, componentes, funciones = filtrar_resultados(resultados)

    return jsonify(
        {
            "definiciones": definiciones,
            "componentes": componentes,
            "funciones": funciones,
        }
    )


# Carga el modelo de spaCy
# xx_ent_wiki_sm: Modelo que reconoce entidades en español, entrenado con datos de Wikipedia
# xx_sent_ud_sm: Modelo que reconoce oraciones en español, entrenado con datos de Universal Dependencies
nlp = spacy.load("xx_sent_ud_sm")


# Identificar el tipo de categoría
def categorizar_texto(texto):
    doc = nlp(texto)

    # Categorías
    categorias = []

    # Inicializar contadores para cada categoría
    conteo_definicion = 0
    conteo_componentes = 0
    conteo_funcionalidades = 0

    # Contar ocurrencias de palabras clave en el texto
    for token in doc:
        if token.text.lower() in palabras_clave_definicion:
            conteo_definicion += 1
        elif token.text.lower() in palabras_clave_componentes:
            conteo_componentes += 1
        elif token.text.lower() in palabras_clave_funcionalidades:
            conteo_funcionalidades += 1

    # Determinar la categoría predominante
    if conteo_definicion > 0:
        categorias.append("DEFINICIONES")
    if conteo_componentes > 0:
        categorias.append("COMPONENTES")
    if conteo_funcionalidades > 0:
        categorias.append("FUNCIONES")

    return categorias


def buscar_bing(palabra=""):
    # Trim al inicio y final
    palabra = palabra.strip().lower().replace(" ", "+")
    resultados_list = []
    for pagina in range(1, 10):
        offset = pagina - 1
        url = f"https://www.bing.com/search?q={palabra}&first={offset}&setlang=es&mkt=es-ES"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=30)
        except requests.exceptions.ChunkedEncodingError:
            print("Ocurrió un error ChunkedEncodingError")
            
        soup = BeautifulSoup(response.text, "lxml")
        resultados = soup.find_all("li", class_="b_algo")
        resultados_list.extend(resultados)

    return resultados_list


def filtrar_resultados(resultados):
    print("Filtrando resultados...")
    resultados_filtrados = []
    resultados_sin_duplicados = []
    links_temp = []
    definiciones = []
    partes = []
    funcionalidades = []

    # Extrae el titulo, link y descripción de cada resultado
    for resultado in resultados:
        try:
            titulo = resultado.find("h2").get_text()
            link = resultado.find("a")["href"]
            descripcion = resultado.find("p").get_text()

            resultados_filtrados.append(
                {"titulo": titulo, "link": link, "descripcion": descripcion}
            )
        except:
            pass

    # Elimina resultados duplicados según el link
    for resultado in resultados_filtrados:
        if resultado["link"] not in links_temp:
            links_temp.append(resultado["link"])
            resultados_sin_duplicados.append(resultado)

    # Categoriza cada resultado
    for resultado in resultados_sin_duplicados:
        try:
            titulo = resultado["titulo"]
            link = resultado["link"]
            descripcion = resultado["descripcion"]
            categorias = categorizar_texto(titulo + descripcion)

            # Asigna el resultado a la/s categoría/s correspondiente/s
            if "DEFINICIONES" in categorias:
                definiciones.append(resultado)
            if "COMPONENTES" in categorias:
                partes.append(resultado)
            if "FUNCIONES" in categorias:
                funcionalidades.append(resultado)
        except:
            pass

    return definiciones, partes, funcionalidades


    """
    =========================================================================
    ============================ I N G L E S ================================
    =========================================================================
    
    """

@app.route("/buscarIng", methods=["POST"])
def buscarIng():
    palabra = request.get_json()["palabra"]
    print(f"Palabra: {palabra}")

    # Realiza búsqueda en Bing como ejemplo
    print("Buscando en Bing...")
    resultados = buscar_bing2(palabra)

    # Filtra resultados
    definiciones, componentes, funciones = filtrar_resultados2(resultados)

    return jsonify(
        {
            "definiciones": definiciones,
            "componentes": componentes,
            "funciones": funciones,
        }
    )


# Carga el modelo de spaCy
# xx_ent_wiki_sm: Modelo que reconoce entidades en español, entrenado con datos de Wikipedia
# xx_sent_ud_sm: Modelo que reconoce oraciones en español, entrenado con datos de Universal Dependencies
nlp = spacy.load("xx_sent_ud_sm")


# Identificar el tipo de categoría
def categorizar_texto2(texto):
    doc = nlp(texto)

    # Categorías
    categorias = []

    # Inicializar contadores para cada categoría
    conteo_definicion = 0
    conteo_componentes = 0
    conteo_funcionalidades = 0

    # Contar ocurrencias de palabras clave en el texto
    for token in doc:
        if token.text.lower() in palabras_clave_definicion2:
            conteo_definicion += 1
        elif token.text.lower() in palabras_clave_componentes2:
            conteo_componentes += 1
        elif token.text.lower() in palabras_clave_funcionalidades2:
            conteo_funcionalidades += 1

    # Determinar la categoría predominante
    if conteo_definicion > 0:
        categorias.append("DEFINICIONES")
    if conteo_componentes > 0:
        categorias.append("COMPONENTES")
    if conteo_funcionalidades > 0:
        categorias.append("FUNCIONES")

    return categorias


def buscar_bing2(palabra=""):
    # Trim al inicio y final
    palabra = palabra.strip().lower().replace(" ", "+")
    resultados_list = []
    for pagina in range(1, 10):
        offset = pagina - 1
        url = f"https://www.bing.com/search?q={palabra}&first={offset}&setlang=en&mkt=en-US"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, "lxml")
        resultados = soup.find_all("li", class_="b_algo")
        resultados_list.extend(resultados)

    return resultados_list


def filtrar_resultados2(resultados):
    print("Filtrando resultados...")
    resultados_filtrados = []
    resultados_sin_duplicados = []
    links_temp = []
    definiciones = []
    partes = []
    funcionalidades = []

    # Extrae el titulo, link y descripción de cada resultado
    for resultado in resultados:
        try:
            titulo = resultado.find("h2").get_text()
            link = resultado.find("a")["href"]
            descripcion = resultado.find("p").get_text()

            resultados_filtrados.append(
                {"titulo": titulo, "link": link, "descripcion": descripcion}
            )
        except:
            pass

    # Elimina resultados duplicados según el link
    for resultado in resultados_filtrados:
        if resultado["link"] not in links_temp:
            links_temp.append(resultado["link"])
            resultados_sin_duplicados.append(resultado)

    # Categoriza cada resultado
    for resultado in resultados_sin_duplicados:
        try:
            titulo = resultado["titulo"]
            link = resultado["link"]
            descripcion = resultado["descripcion"]
            categorias = categorizar_texto2(titulo + descripcion)

            # Asigna el resultado a la/s categoría/s correspondiente/s
            if "DEFINICIONES" in categorias:
                definiciones.append(resultado)
            if "COMPONENTES" in categorias:
                partes.append(resultado)
            if "FUNCIONES" in categorias:
                funcionalidades.append(resultado)
        except:
            pass

    return definiciones, partes, funcionalidades


if __name__ == "__main__":
    app.run(debug=True)
