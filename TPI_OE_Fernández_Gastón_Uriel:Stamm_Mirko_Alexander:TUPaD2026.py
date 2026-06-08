import csv
import os
from datetime import datetime
from enum import Enum

# --- DEFINICION DE ENUMS ---
class EstadoTurno(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"

class OpcionMenu(Enum):
    VER_TURNOS = "1"
    TOMAR_TURNO = "2"
    CONFIRMAR_TURNO = "3"
    CANCELAR_TURNO = "4"
    SALIR = "5"

# --- CONFIGURACION DE ARCHIVOS ---
ARCHIVO_ESPECIALISTAS = "especialistas.csv"

# --- CARGA DE BASE DE DATOS DESDE CSV ---
def cargar_especialistas():
    plantilla = {}
    # Verificamos si existe el archivo y si tiene un tamaño mayor a 0 bytes
    if os.path.exists(ARCHIVO_ESPECIALISTAS) and os.path.getsize(ARCHIVO_ESPECIALISTAS) > 0:
        try:
            with open(ARCHIVO_ESPECIALISTAS, mode="r", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    # Validacion de que las columnas requeridas existan en la fila
                    if "animal" in fila and "especialista" in fila and "turnos" in fila:
                        animal = fila["animal"].strip().lower()
                        especialista = fila["especialista"].strip()
                        lista_turnos = [t.strip() for t in fila["turnos"].split(";") if t.strip()]
                        
                        if animal and especialista and lista_turnos:
                            plantilla[animal] = {
                                "especialista": especialista,
                                "turnos": lista_turnos
                            }
        except Exception:
            print("Error critico al leer el archivo. Cargando datos de respaldo.")
    
    # Si por alguna razon la plantilla quedo vacia, forzamos los datos de respaldo
    if not plantilla:
        return {
            "perro": {"especialista": "Dr. Perez (Caninos)", "turnos": ["10:00", "14:00"]},
            "gato": {"especialista": "Dra. Martinez (Felinos)", "turnos": ["11:00", "16:00"]},
            "ave": {"especialista": "Dr. Silva (Aves)", "turnos": ["09:30", "15:00"]},
            "roedor": {"especialista": "Dra. Rossi (Roedores)", "turnos": ["11:00", "18:30"]},
            "reptil": {"especialista": "Dr. Mendez (Reptiles)", "turnos": ["09:00", "16:00"]}
        }
    return plantilla

# --- VARIABLES GLOBALES ---
PLANTILLA_ESPECIALISTAS = cargar_especialistas()
TURNOS_AGENDADOS = []

# --- VALIDACION ---
def validar_fecha(fecha_str):
    try:
        ano_actual = datetime.now().year
        datetime.strptime(f"{fecha_str}/{ano_actual}", "%d/%m/%Y")
        return True
    except ValueError:
        print("Error: Formato de fecha invalido (Debe ser DD/MM).")
        return False

# --- PROCESOS DEL MENU ---

def ver_turnos_disponibles():
    print("\n--- 1. CONSULTAR TURNOS DISPONIBLES ---")
    fecha = input("Ingrese la fecha a consultar (DD/MM): ").strip()
    if not validar_fecha(fecha): return False

    print(f"\n=== HORARIOS DISPONIBLES PARA EL DIA {fecha} ===")
    for especie, info in PLANTILLA_ESPECIALISTAS.items():
        print(f"\nEspecie: {especie.upper()} -> {info['especialista']}:")
        horarios_ocupados = [t["horario"] for t in TURNOS_AGENDADOS if t["fecha"] == fecha and t["especie"] == especie]
        
        hay_turnos = False
        for horario in info["turnos"]:
            if horario not in horarios_ocupados:
                print(f"   [ ] {horario} hs")
                hay_turnos = True
        if not hay_turnos:
            print("   No quedan horarios disponibles para esta especie.")
    return True

def tomar_turno():
    print("\n--- 2. RESERVAR UN TURNO ---")
    fecha = input("Ingrese la fecha (DD/MM): ").strip()
    if not validar_fecha(fecha): return False

    especies_disponibles = ", ".join(PLANTILLA_ESPECIALISTAS.keys())
    print(f"Especies en sistema: {especies_disponibles}")
    animal = input("Ingrese el tipo de animal: ").strip().lower()

    if animal not in PLANTILLA_ESPECIALISTAS:
        print(f"Error: No se atiende la especie '{animal}'.")
        return False

    horarios_ocupados = [t["horario"] for t in TURNOS_AGENDADOS if t["fecha"] == fecha and t["especie"] == animal]
    horarios_libres = [h for h in PLANTILLA_ESPECIALISTAS[animal]["turnos"] if h not in horarios_ocupados]

    if not horarios_libres:
        print(f"Error: No quedan turnos para {animal} el dia {fecha}.")
        return False

    print(f"\nTurnos disponibles para {animal.upper()} el {fecha}:")
    for i, horario in enumerate(horarios_libres, start=1):
        print(f"[{i}] {horario} hs")

    try:
        seleccion = int(input("Seleccione el numero de turno: "))
        if 1 <= seleccion <= len(horarios_libres):
            horario_elegido = horarios_libres[seleccion - 1]
            
            nuevo_turno = {
                "fecha": fecha,
                "especie": animal,
                "horario": horario_elegido,
                "estado": EstadoTurno.PENDIENTE.value
            }
            TURNOS_AGENDADOS.append(nuevo_turno)
            print(f"Exito: Turno reservado para {animal.upper()} a las {horario_elegido}hs.")
            return True
        else:
            print("Error: Opcion fuera de rango.")
            return False
    except ValueError:
        print("Error: Debe ingresar un numero entero.")
        return False

def buscar_y_listar_turnos(fecha):
    turnos_filtrados = [t for t in TURNOS_AGENDADOS if t["fecha"] == fecha]
    if not turnos_filtrados:
        print(f"Aviso: No hay turnos registrados para el dia {fecha}.")
        return None

    print(f"\nTurnos encontrados para el {fecha}:")
    for i, t in enumerate(turnos_filtrados, start=1):
        print(f"[{i}] {t['especie'].upper()} a las {t['horario']}hs | Estado: {t['estado']}")
    
    try:
        seleccion = int(input("Seleccione el numero de turno a gestionar: "))
        if 1 <= seleccion <= len(turnos_filtrados):
            return turnos_filtrados[seleccion - 1]
        print("Error: Opcion invalida.")
    except ValueError:
        print("Error: Entrada invalida.")
    return None

def confirmar_turno():
    print("\n--- 3. CONFIRMAR TURNO ---")
    fecha = input("Ingrese la fecha del turno (DD/MM): ").strip()
    if not validar_fecha(fecha): return False

    turno = buscar_y_listar_turnos(fecha)
    if turno:
        turno["estado"] = EstadoTurno.CONFIRMADO.value
        print(f"Exito: El turno de {turno['especie'].upper()} a las {turno['horario']}hs ha sido CONFIRMADO.")
        return True
    return False

def cancelar_turno():
    print("\n--- 4. CANCELAR TURNO ---")
    fecha = input("Ingrese la fecha del turno (DD/MM): ").strip()
    if not validar_fecha(fecha): return False

    turno = buscar_y_listar_turnos(fecha)
    if turno:
        TURNOS_AGENDADOS.remove(turno)
        print(f"Exito: El turno de {turno['especie'].upper()} a las {turno['horario']}hs ha sido CANCELADO.")
        return True
    return False

# --- FLUJO PRINCIPAL ---

def desea_continuar():
    while True:
        rta = input("\n¿Desea realizar otra accion? (S/N): ").strip().upper()
        if rta in ["S", "SI"]: return True
        if rta in ["N", "NO"]: return False
        print("Error: Ingrese S o N.")

def main():
    while True:
        print("\n--- VETERINARIA - MENU PRINCIPAL ---")
        print("1. Ver turnos disponibles de un día")
        print("2. Tomar Turno")
        print("3. Confirmar Turno")
        print("4. Cancelar Turno")
        print("5. Salir")
        
        opcion = input("Escoge una opcion (1-5): ").strip()
        exito_operacion = False

        if opcion == OpcionMenu.VER_TURNOS.value:
            exito_operacion = ver_turnos_disponibles()
        elif opcion == OpcionMenu.TOMAR_TURNO.value:
            exito_operacion = tomar_turno()
        elif opcion == OpcionMenu.CONFIRMAR_TURNO.value:
            exito_operacion = confirmar_turno()
        elif opcion == OpcionMenu.CANCELAR_TURNO.value:
            exito_operacion = cancelar_turno()
        elif opcion == OpcionMenu.SALIR.value:
            print("\nGracias por usar el sistema. Que tenga un buen dia.")
            break
        else:
            print("Error: Opcion Invalida. Intente de nuevo.")
            continue 

        if exito_operacion:
            if not desea_continuar():
                print("\nGracias por usar el sistema. Que tenga un buen dia.")
                break
        else:
            print("Regresando al menu principal por error en los datos de la operacion...")

if __name__ == "__main__":
    main()
