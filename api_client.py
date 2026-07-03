import urllib.request
import urllib.parse
import json


API_URL = "https://api.example.com/analyze"


def analizar_con_api(comentario):
    data = urllib.parse.urlencode({"texto": comentario}).encode()
    try:
        req = urllib.request.Request(API_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            resultado = json.loads(response.read().decode())
            return resultado.get("categoria"), resultado.get("prioridad")
    except Exception as e:
        print(f"[api_client] Error al conectar con la API: {e}")
        return None, None


if __name__ == "__main__":
    cat, pri = analizar_con_api("prueba")
    print(f"Resultado API: {cat} / {pri}")
