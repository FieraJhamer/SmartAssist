def analizar_comentario(texto):

    texto = texto.lower()

    if "ingresar" in texto:

        categoria = "ERROR_ACCESO"
        prioridad = "ALTA"

    elif "lento" in texto or "demora" in texto or "lenta" in texto:

        categoria = "RENDIMIENTO"
        prioridad = "MEDIA"

    elif "factura" in texto or "cobro" in texto or "pago" in texto or "tarjeta" in texto or "compra" in texto:

        categoria = "FACTURACION"
        prioridad = "ALTA"
    
    elif "dañado" in texto or "equivocado" in texto or "incompleto" in texto or "faltante" in texto or "destruido" in texto:
        categoria = "DEVOLUCION"  
        prioridad = "ALTA" 
    
    elif "baja" in texto or "liquidar" in texto or "saldar" in texto or "rescindir" in texto:
        categoria = "CANCELACION"
        prioridad = "ALTA"

    else:

        categoria = "CONSULTA"
        prioridad = "BAJA"

    return {
        "comentario": texto,
        "categoria": categoria,
        "prioridad": prioridad
    }
