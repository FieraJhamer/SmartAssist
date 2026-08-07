import base_datos
import clasificador


EJEMPLOS = [
    ("No hay agua en mi barrio desde hace dos días", "Av. Ortiz de Ocampo", "1250"),
    ("Se filtra agua por la vereda frente a mi casa", "Calle Rivadavia", "345"),
    ("La plaza está llena de basura y contenedores desbordados", "Plaza 25 de Mayo", "0"),
    ("No pasan los recolectores de residuos hace una semana", "Calle Catamarca", "780"),
    ("Se cortó el alumbrado público en toda la cuadra", "Av. San Nicolás", "2100"),
    ("El farol de la esquina está apagado desde hace un mes", "Calle 9 de Julio", "560"),
    ("Hubo un robo a mano armada en el kiosco de la esquina", "Calle Copiapó", "112"),
    ("Hay cables pelados colgando en la zona, es un peligro", "Av. Ramírez de Velasco", "880"),
    ("La calle tiene baches enormes que dañan los autos", "Calle Pueyrredón", "430"),
    ("La vereda de la escuela está rota y hundida", "Calle Buenos Aires", "610"),
    ("El colectivo de la línea 3 tarda una hora en pasar", "Av. Monseñor Tiburcio Benegas", "1500"),
    ("Falta una parada de colectivo en el barrio", "Calle Pelagio B. Luna", "950"),
    ("El terreno baldío tiene maleza y escombros acumulados", "Calle Bazán y Bustos", "220"),
    ("Necesitan podar los árboles del parque central", "Parque de la Ciudad", "0"),
    ("Quiero información sobre los turnos municipales", "Calle Rivadavia", "100"),
    ("La luminaria de la plaza no enciende de noche", "Plaza Vélez Sarsfield", "0"),
    ("Hay un basural clandestino detrás de la terminal", "Calle Almirante Brown", "1300"),
    ("El desagüe cloacal de la calle está tapado y desborda", "Calle Santa Fe", "710"),
    ("Quiero saber cómo hago para denunciar un perro suelto", "Calle Lamadrid", "320"),
    ("La señalización de tránsito de la avenida está borrada", "Av. Los Puentes", "2750"),
    ("El micro de media distancia para en el centro", "Calle 9 de Julio", "900"),
    ("La maleza tapa la senda peatonal en el barrio Norte", "Calle Dean Funes", "540"),
    ("Hay una pérdida de agua en la calle Alberdi", "Calle Alberdi", "415"),
    ("Un transformador hace ruido y tira chispas", "Calle Chile", "670"),
    ("Vandalizaron la garita de la parada de colectivos", "Av. Santa Catalina", "1850"),
    ("El bache de la esquina rompió la rueda de mi auto", "Calle Maipú", "260"),
    ("Los contenedores de residuos están siempre llenos", "Calle Tandil", "840"),
    ("Falta iluminación en el pasaje del fondo", "Pasaje El Sauce", "30"),
    ("Piden fumigación por los mosquitos en la plaza", "Plaza Güemes", "0"),
    ("Quiero saber qué categoría corresponde a mi reclamo", "Calle Dalmacio Vélez", "150"),
]


def cargar():
    base_datos.crear_tabla()
    contados = {}
    for texto, calle, numero in EJEMPLOS:
        categoria, prioridad = clasificador.clasificar_comentario(texto)
        base_datos.insertar_reclamo(texto, categoria, prioridad, calle, numero)
        contados[categoria] = contados.get(categoria, 0) + 1
    print(f"Se cargaron {len(EJEMPLOS)} reclamos de ejemplo:")
    for cat, cant in sorted(contados.items()):
        print(f"  {cat}: {cant}")


if __name__ == "__main__":
    cargar()
