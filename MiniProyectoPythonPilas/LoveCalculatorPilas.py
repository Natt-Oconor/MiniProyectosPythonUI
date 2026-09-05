# love_calculator_avanzado_pilas.py
import unicodedata


class Pila:
    """Implementación de una Pila (Stack) LIFO."""

    def __init__(self):
        self._datos = []

    def apilar(self, x):
        self._datos.append(x)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Pila vacía")
        return self._datos.pop()

    def tope(self):
        """Consulta el elemento en el tope sin removerlo."""
        if self.esta_vacia():
            return None
        return self._datos[-1]

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0

    def __len__(self) -> int:
        return len(self._datos)


# ---------- Utilidades y Datos Zodiacales ----------

ELEMENTOS_SIGNOS = {
    "aries": "fuego",
    "leo": "fuego",
    "sagitario": "fuego",
    "tauro": "tierra",
    "virgo": "tierra",
    "capricornio": "tierra",
    "geminis": "aire",
    "libra": "aire",
    "acuario": "aire",
    "cancer": "agua",
    "escorpio": "agua",
    "piscis": "agua",
}


def normalizar_texto(texto: str) -> str:
    """Elimina tildes y espacios extras, pasando a minúsculas."""
    texto = texto.strip().lower()
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def signo_compatible(signo1: str, signo2: str) -> bool:
    s1 = normalizar_texto(signo1)
    s2 = normalizar_texto(signo2)

    e1 = ELEMENTOS_SIGNOS.get(s1)
    e2 = ELEMENTOS_SIGNOS.get(s2)

    if e1 is None or e2 is None:
        return False

    return e1 == e2


# ---------- Procesamiento con Pilas ----------

def procesar_nombre_con_pila(nombre: str) -> str:
    """Invierte el nombre utilizando una pila (ejercicio didáctico)."""
    pila = Pila()
    for c in nombre:
        pila.apilar(c)

    invertido_chars = []
    while not pila.esta_vacia():
        invertido_chars.append(pila.desapilar())

    nombre_invertido = "".join(invertido_chars)
    print(f"Nombre original: {nombre} -> Invertido con Pila: {nombre_invertido}")
    return nombre


def calcular_compatibilidad_nombres(nombre1: str, nombre2: str) -> int:
    combinados = (nombre1 + nombre2).lower()

    # Conteo de letras de TRUE
    primer_digito = sum(combinados.count(c) for c in "true")
    # Conteo de letras de LOVE
    segundo_digito = sum(combinados.count(c) for c in "love")

    return (primer_digito % 10) * 10 + (segundo_digito % 10)


def construir_mensaje_con_pila(puntaje: int, detalles: list[str]) -> str:
    """Usa una pila para armar el mensaje de compatibilidad."""
    pila_mensaje = Pila()

    # 1. Apilamos el final del mensaje primero
    pila_mensaje.apilar(f"Compatibilidad total: {puntaje}%")

    # 2. Apilamos los detalles en orden inverso
    for d in reversed(detalles):
        pila_mensaje.apilar(d)

    # 3. Apilamos la conclusión al final (para que sea lo primero en desapilar)
    if puntaje < 20 or puntaje > 85:
        pila_mensaje.apilar("💥 Pareja explosiva")
    elif 45 <= puntaje <= 65:
        pila_mensaje.apilar("❤️ Tienen excelente química")
    else:
        pila_mensaje.apilar("💪 Pueden funcionar con paciencia y esfuerzo")

    # Desapilamos para obtener el orden natural
    partes = []
    while not pila_mensaje.esta_vacia():
        partes.append(pila_mensaje.desapilar())

    return " | ".join(partes)


# ---------- Entrada y Validaciones ----------

def leer_persona(numero: int) -> dict:
    print(f"\n--- Datos de la persona {numero} ---")
    
    while True:
        nombre = input("Nombre: ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío.")

    while True:
        try:
            edad = int(input("Edad: "))
            if 0 < edad < 120:
                break
            print("Por favor, introduce una edad válida (1 - 120).")
        except ValueError:
            print("Entrada inválida. Escribe un número entero.")

    while True:
        signo = input("Signo zodiacal: ").strip()
        if normalizar_texto(signo) in ELEMENTOS_SIGNOS:
            break
        signos_validos = ", ".join([s.capitalize() for s in ELEMENTOS_SIGNOS.keys()])
        print(f"Signo no reconocido. Opciones válidas: {signos_validos}")

    while True:
        personalidad = input("Personalidad (introvertido/extrovertido): ").strip().lower()
        if personalidad in ("introvertido", "extrovertido"):
            break
        print("Opción no válida. Escribe 'introvertido' o 'extrovertido'.")

    while True:
        estilo = input("Estilo (planificador/espontaneo): ").strip().lower()
        if estilo in ("planificador", "espontaneo"):
            break
        print("Opción no válida. Escribe 'planificador' o 'espontaneo'.")

    return {
        "nombre": nombre,
        "edad": edad,
        "signo": signo.capitalize(),
        "personalidad": personalidad,
        "estilo": estilo,
    }


def calcular_compatibilidad_total(p1: dict, p2: dict) -> int:
    puntaje = calcular_compatibilidad_nombres(p1["nombre"], p2["nombre"])

    if signo_compatible(p1["signo"], p2["signo"]):
        puntaje += 15

    if p1["personalidad"] == p2["personalidad"]:
        puntaje += 5
    else:
        puntaje -= 2

    if p1["estilo"] == p2["estilo"]:
        puntaje += 5
    else:
        puntaje -= 2

    if abs(p1["edad"] - p2["edad"]) > 10:
        puntaje -= 5

    return max(0, min(100, puntaje))


def generar_detalles(p1: dict, p2: dict) -> list[str]:
    detalles = []

    if signo_compatible(p1["signo"], p2["signo"]):
        detalles.append(f"Signos compatibles (+15)")
    else:
        detalles.append("Signos de elementos distintos")

    if p1["personalidad"] == p2["personalidad"]:
        detalles.append(f"Misma personalidad: {p1['personalidad']} (+5)")
    else:
        detalles.append(f"Personalidad distinta: {p1['personalidad']} vs {p2['personalidad']} (-2)")

    if p1["estilo"] == p2["estilo"]:
        detalles.append(f"Mismo estilo: {p1['estilo']} (+5)")
    else:
        detalles.append(f"Estilo distinto: {p1['estilo']} vs {p2['estilo']} (-2)")

    diff_edad = abs(p1["edad"] - p2["edad"])
    if diff_edad > 10:
        detalles.append(f"Diferencia de edad ({diff_edad} años) (-5)")
    else:
        detalles.append(f"Diferencia de edad óptima ({diff_edad} años)")

    return detalles


# ---------- Gestión del Historial con Pila ----------

def guardar_historial_con_pila(historial: Pila, p1: dict, p2: dict, puntaje: int):
    registro = (
        f"{p1['nombre']} ({p1['signo']}, {p1['edad']}a) + "
        f"{p2['nombre']} ({p2['signo']}, {p2['edad']}a) => {puntaje}%"
    )
    historial.apilar(registro)


def mostrar_historial_con_pila(historial: Pila):
    if historial.esta_vacia():
        print("\n[!] No hay historial de parejas aún.")
        return

    print(f"\n=== Historial de Parejas ({len(historial)} registros) ===")
    temporal = Pila()
    
    # Desapilamos mostrando el más reciente primero
    while not historial.esta_vacia():
        item = historial.desapilar()
        print(f" • {item}")
        temporal.apilar(item)

    # Restauramos la pila original
    while not temporal.esta_vacia():
        historial.apilar(temporal.desapilar())


def deshacer_ultimo_calculo(historial: Pila):
    if historial.esta_vacia():
        print("\n[!] No hay cálculos que deshacer.")
        return
    eliminado = historial.desapilar()
    print(f"\n[✓] Se eliminó el último registro: {eliminado}")


# ---------- Menú Principal ----------

def main():
    print("========================================")
    print("   💘 Love Calculator con Pilas 💘")
    print("========================================")

    historial = Pila()

    while True:
        print("\nOpciones:")
        print("1. Calcular compatibilidad de una nueva pareja")
        print("2. Ver historial de parejas")
        print("3. Deshacer / Eliminar último cálculo")
        print("4. Salir")

        opcion = input("Elige una opción (1/2/3/4): ").strip()

        if opcion == "1":
            p1 = leer_persona(1)
            p2 = leer_persona(2)

            print("\n--- Demostración de Pila con Nombres ---")
            procesar_nombre_con_pila(p1["nombre"])
            procesar_nombre_con_pila(p2["nombre"])

            puntaje = calcular_compatibilidad_total(p1, p2)
            detalles = generar_detalles(p1, p2)
            mensaje = construir_mensaje_con_pila(puntaje, detalles)

            print("\n================ RESULTADO ================")
            print(mensaje)
            print("===========================================")

            guardar_historial_con_pila(historial, p1, p2, puntaje)

        elif opcion == "2":
            mostrar_historial_con_pila(historial)

        elif opcion == "3":
            deshacer_ultimo_calculo(historial)

        elif opcion == "4":
            print("\n¡Gracias por usar Love Calculator! Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()