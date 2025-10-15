# Requiere: colorama


import os
import random
import time
import json
import sys
from colorama import Fore, Back, Style, init

# Inicializa colorama
init(autoreset=True)

SCORES_FILE = "mision_adn_scores.json"

TABLA_GENETICA = {
    "AUG": "Met", "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
    "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile",
    "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
    "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "UAU": "Tyr", "UAC": "Tyr", "UAA": "Stop", "UAG": "Stop",
    "UGU": "Cys", "UGC": "Cys", "UGA": "Stop",
    "CAA": "Gln", "CAG": "Gln", "AAU": "Asn", "AAC": "Asn",
    "AAA": "Lys", "AAG": "Lys", "GAU": "Asp", "GAC": "Asp",
    "GAA": "Glu", "GAG": "Glu", "UGG": "Trp",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AGA": "Arg", "AGG": "Arg", "AGU": "Ser", "AGC": "Ser",
    "GGA": "Gly", "GGC": "Gly", "GGU": "Gly", "GGG": "Gly"
}

# ---------------------------
# Utilidades de pantalla
# ---------------------------

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo():
    limpiar_pantalla()
    print(Fore.GREEN + Style.BRIGHT + "=" * 80)
    print(Fore.YELLOW + Style.BRIGHT + "  M I S I Ó N   A D N :  N I V E L E S   Y   R E T O S  ".center(80))
    print(Fore.GREEN + Style.BRIGHT + "=" * 80)

def pausa(msg="Presiona ENTER para continuar..."):
    try:
        input(Fore.CYAN + msg)
    except EOFError:
        pass

def beep():
    print('\a', end='')

# ---------------------------
# Puntajes
# ---------------------------

def cargar_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_score(nombre, puntaje):
    scores = cargar_scores()
    scores.append({"nombre": nombre, "puntaje": puntaje, "tiempo": time.strftime("%Y-%m-%d %H:%M:%S")})
    scores = sorted(scores, key=lambda x: x["puntaje"], reverse=True)[:20]
    with open(SCORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

# ---------------------------
# Generar genes
# ---------------------------

BASES = ['A', 'T', 'C', 'G']
TRANSCR_MAP = {"A": "U", "T": "A", "C": "G", "G": "C"}

def generar_gene(longitud_codones=4, include_promoter=True, mutation_rate=0.0):
    dna = []
    if include_promoter:
        promoter = random.choice(["TATA", "TATAAA", "TATATA"])
        dna.append(promoter)
    for _ in range(longitud_codones * 3):
        base = random.choice(BASES)
        if random.random() < mutation_rate:
            base = random.choice([b for b in BASES if b != base])
        dna.append(base)
    return "".join(dna)

def formatear_con_espacios(s, n=3):
    return " ".join([s[i:i+n] for i in range(0, len(s), n)])

def transcribir(adn):
    adn_clean = adn.replace(" ", "").upper()
    return "".join([TRANSCR_MAP.get(b, "N") for b in adn_clean])

def traducir(arn):
    arn = arn.replace(" ", "").upper()
    codones = [arn[i:i+3] for i in range(0, len(arn), 3)]
    proteina = []
    for c in codones:
        aa = TABLA_GENETICA.get(c, "??")
        if aa == "Stop" or len(c) < 3:
            break
        proteina.append(aa)
    return proteina, codones

# ---------------------------
# Animaciones
# ---------------------------

def animar_ribosoma(codones, velocidad=0.6):
    ribo_shape = "[=R=]"
    cadena = " ".join(codones)
    parts = cadena.split(" ")
    for i in range(len(parts)+3):
        limpiar_pantalla()
        imprimir_titulo()
        print(Fore.CYAN + "Animando traducción... (ribosoma moviéndose)\n")
        line = ""
        for j, cod in enumerate(parts):
            if j == i:
                line += Back.WHITE + Fore.BLACK + ribo_shape + Style.RESET_ALL + " "
            line += Fore.YELLOW + cod + " "
        print(line + "\n")
        time.sleep(velocidad)

# ---------------------------
# Juego principal por niveles
# ---------------------------

def nivel_intro(nivel):
    imprimir_titulo()
    print(Fore.MAGENTA + f"Nivel {nivel}: Objetivo y condiciones\n")
    if nivel == 1:
        print("Aprenderás a identificar promotores, transcribir y traducir una secuencia corta.")
    elif nivel == 2:
        print("Secuencias más largas y posibilidad de mutaciones.")
    elif nivel == 3:
        print("Secuencias extensas y traducción con opciones múltiples.")
    pausa()

def jugar_nivel(nivel, jugador):
    puntos = 0
    if nivel == 1:
        codones, mutation_rate = 3, 0.0
    elif nivel == 2:
        codones, mutation_rate = 5, 0.08
    else:
        codones, mutation_rate = 7, 0.12

    nivel_intro(nivel)

    seqs = []
    correcta_idx = random.randint(0, 2)
    for i in range(3):
        seqs.append(generar_gene(codones, i == correcta_idx, mutation_rate))

    imprimir_titulo()
    print(Fore.CYAN + f"ETAPA A: Identificación del gen (Nivel {nivel})\n")
    for i, s in enumerate(seqs):
        print(f"{i+1}. {formatear_con_espacios(s, 3)}")
    ans = input(Fore.YELLOW + "\n¿Cuál contiene el promotor? (1,2 o 3): ").strip()

    if ans == str(correcta_idx+1):
        print(Fore.GREEN + " Correcto: detectaste el promotor.")
        puntos += 2
    else:
        print(Fore.RED + f" Incorrecto. Era la {correcta_idx+1}.")
    pausa()

    adn = seqs[correcta_idx]
    imprimir_titulo()
    print(Fore.CYAN + "ETAPA B: Transcripción (ADN → ARN)\n")
    print(Fore.YELLOW + formatear_con_espacios(adn, 3))
    resp = input("\nEscribe la secuencia de ARN complementaria: ").upper().replace(" ", "")
    arn_correcto = transcribir(adn)

    if resp == arn_correcto:
        print(Fore.GREEN + " Transcripción correcta.")
        puntos += 2
    else:
        print(Fore.RED + " Transcripción incorrecta.")
        print(Fore.CYAN + f"Secuencia correcta: {formatear_con_espacios(arn_correcto, 3)}")
    pausa()

    imprimir_titulo()
    print(Fore.CYAN + "ETAPA C: Traducción (ARN → Proteína)\n")
    codones_arn = [arn_correcto[i:i+3] for i in range(0, len(arn_correcto), 3)]
    print(Fore.YELLOW + " ".join(codones_arn))
    pausa("Ver animación del ribosoma. ENTER para iniciar...")
    animar_ribosoma(codones_arn, velocidad=max(0.4, 1.0 - nivel * 0.15))

    proteina_jugador, proteina_correcta = [], []
    opciones_cache = []
    for cod in codones_arn:
        aa_correcto = TABLA_GENETICA.get(cod, "??")
        proteina_correcta.append(aa_correcto)
        posibles = list(set([v for v in TABLA_GENETICA.values() if v != "Stop"]))
        opciones = [aa_correcto] if aa_correcto != "??" else []
        while len(opciones) < 4:
            cand = random.choice(posibles)
            if cand not in opciones:
                opciones.append(cand)
        random.shuffle(opciones)
        opciones_cache.append(opciones)

    imprimir_titulo()
    print(Fore.CYAN + "Selecciona el aminoácido para cada codón:\n")
    for i, cod in enumerate(codones_arn):
        print(Fore.YELLOW + f"{i+1}. Codón {cod}")
        for j, op in enumerate(opciones_cache[i]):
            print(f"    {j+1}. {op}")
        elec = input("   Tu elección (1-4): ").strip()
        try:
            elegido = opciones_cache[i][int(elec)-1]
        except:
            elegido = "??"
        proteina_jugador.append(elegido)

    imprimir_titulo()
    print(Fore.MAGENTA + f"Tu proteína:      {Fore.YELLOW}{' - '.join(proteina_jugador)}")
    print(Fore.GREEN + f"Proteína esperada: {Fore.YELLOW}{' - '.join(proteina_correcta)}")

    aciertos = sum(1 for j, c in zip(proteina_jugador, proteina_correcta) if j == c and c != "??")
    total = sum(1 for c in proteina_correcta if c != "??")
    ratio = aciertos / total if total else 0
    puntos += int(round(ratio * 6))

    if ratio == 1:
        print(Fore.GREEN + "\n ¡Perfecto!")
        beep()
    elif ratio >= 0.6:
        print(Fore.CYAN + "\nBuen trabajo.")
    else:
        print(Fore.RED + "\nNecesitás repasar la traducción.")
    pausa()
    return puntos

# ---------------------------
# Puntajes y menú principal
# ---------------------------

def ver_mejores():
    imprimir_titulo()
    print(Fore.MAGENTA + " Mejores puntajes\n")
    scores = cargar_scores()
    if not scores:
        print("Aún no hay puntajes guardados.")
    else:
        for i, s in enumerate(scores):
            print(Fore.YELLOW + f"{i+1}. {s['nombre']} — {s['puntaje']} pts — {s['tiempo']}")
    pausa()

def menu_principal():
    jugador = ""
    while True:
        imprimir_titulo()
        if not jugador:
            jugador = input(Fore.YELLOW + "Nombre del jugador: ").strip() or "Anónimo"

        print("\nMenú:")
        print("  1) Jugar (3 niveles)")
        print("  2) Ver mejores puntajes")
        print("  3) Salir")
        op = input(Fore.YELLOW + "\nElegí una opción (1-3): ").strip()

        if op == "1":
            total = 0
            for nivel in [1, 2, 3]:
                puntos = jugar_nivel(nivel, jugador)
                total += puntos
                imprimir_titulo()
                print(Fore.CYAN + f"Completaste Nivel {nivel}. Puntos: {puntos}")
                print(Fore.GREEN + f"Puntaje acumulado: {total}")
                pausa()
            imprimir_titulo()
            print(Fore.YELLOW + f"🏁 Fin de la campaña. Puntaje total: {total}")
            guardar = input(Fore.YELLOW + "¿Guardar puntaje en el ranking? (s/n): ").strip().lower()
            if guardar == "s":
                guardar_score(jugador, total)
                print(Fore.GREEN + "Puntaje guardado.")
            pausa()
        elif op == "2":
            ver_mejores()
        elif op == "3":
            limpiar_pantalla()
            print(Fore.GREEN + "Gracias por jugar")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Opción inválida.")
            time.sleep(1)

# ---------------------------
# Inicio del programa
# ---------------------------

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Interrumpido por usuario. Saliendo...")
        time.sleep(0.5)
        sys.exit(0)
