import urllib.request
import urllib.parse
import json


URL_API_EXTERNA = "https://api.example.com/analyze"


def analizar_comentario_con_api(comentario):
    data = urllib.parse.urlencode({"texto": comentario}).encode()
    try:
        req = urllib.request.Request(URL_API_EXTERNA, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            resultado = json.loads(response.read().decode())
            return resultado.get("categoria"), resultado.get("prioridad")
    except Exception as e:
        print(f"[cliente_api] Error al conectar con la API: {e}")
        return None, None


if __name__ == "__main__":
    cat, pri = analizar_comentario_con_api("prueba")
    print(f"Resultado API: {cat} / {pri}")
