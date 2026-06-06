import csv
import os
import time
import tempfile
from datetime import datetime
from enum import Enum

# --- DEFINICIÓN DE ENUMS ---
class AccionTurno(Enum):
    CONFIRMAR = 1
    CANCELAR = 2

class OpcionesMenu(Enum):
    VER_TURNOS = "1"
    TOMAR_TURNO = "2"
    CONFIRMAR_TURNO = "3"
    CANCELAR_TURNO = "4"
    SALIR = "5"

# --- GESTIÓN DE RUTAS SEGURAS ---
def obtener_ruta_segura(archivo_nombre="turnos_reservados.csv"):
    ruta_local = archivo_nombre
    if os.path.exists(ruta_local) and os.access(ruta_local, os.W_OK):
        return ruta_local
    
    try:
        test_file = os.path.join(".", ".test_write")
        with open(test_file, "w") as f:
            f.write("")
        os.remove(test_file)
        return ruta_local
    except (OSError, IOError):
        return os.path.join(tempfile.gettempdir(), archivo_nombre)

# --- CARGA DINÁMICA DE BASE DE DATOS DESDE CSV ---
def cargar_base_de_datos(archivo_path="especialistas.csv"):
    bd_inicializada = {}
    if os.path.exists(archivo_path):
        try:
            with open(archivo_path, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    animal = fila['animal'].strip().lower()
                    especialista = fila['especialista'].strip()
                    lista_turnos = [t.strip() for t in fila['turnos'].split(';') if t.strip()]
                    
                    bd_inicializada[animal] = {
                        "especialista": especialista,
                        "turnos": lista_turnos
                    }
            return bd_inicializada
        except Exception:
            print("Aviso: Hubo un error al leer especialistas.csv. Cargando datos de respaldo.")
            
    return {
        "perro": {"especialista": "Dr. Perez (Caninos)", "turnos": ["10:00", "14:00"]},
        "gato": {"especialista": "Dra. Martinez (Felinos)", "turnos": ["11:00", "16:00"]},
        "ave": {"especialista": "Dr. Silva (Aves)", "turnos": ["09:30", "15:00"]},
        "roedor": {"especialista": "Dra. Rossi (Roedores)", "turnos": ["11:00", "18:30"]},
        "reptil": {"especialista": "Dr. Mendez (Reptiles)", "turnos": ["09:00", "16:00"]}
    }

# --- PERSISTENCIA DE TURNOS DE USUARIOS ---
def cargar_turnos_usuarios():
    bd_turnos_usuarios = {}
    ruta_archivo = obtener_ruta_segura()
    
    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    fecha = fila['fecha'].strip()
                    nuevo_turno = {
                        "especie": fila['especie'].strip(),
                        "horario": fila['horario'].strip(),
                        "estado": fila['estado'].strip(),
                        "texto": fila['detalle'].strip()
                    }
                    if fecha not in bd_turnos_usuarios:
                        bd_turnos_usuarios[fecha] = []
                    bd_turnos_usuarios[fecha].append(nuevo_turno)
            print(f"[Sistema] Historial cargado correctamente desde: {ruta_archivo}")
        except Exception:
            print("[Sistema] Aviso: No se pudo procesar el archivo de turnos previos.")
    return bd_turnos_usuarios

def guardar_turnos_usuarios():
    ruta_archivo = obtener_ruta_segura()
    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            columnas = ["fecha", "especie", "horario", "estado", "detalle"]
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            
            for fecha, lista_turnos in turnos_agendados_usuario.items():
                for turno in lista_turnos:
                    escritor.writerow({
                        "fecha": fecha,
                        "especie": turno["especie"],
                        "horario": turno["horario"],
                        "estado": turno["estado"],
                        "detalle": turno["texto"]
                    })
        print(f"[Sistema] Cambios guardados en: {ruta_archivo}")
    except Exception as e:
        print(f"[Sistema] Nota: No se pudo escribir en disco ({e}). Datos mantenidos en memoria RAM.")

# --- RECONSTRUCCIÓN DE GRILLA DE DISPONIBILIDAD DIARIA ---
def sincronizar_disponibilidad_diaria():
    global turnos_disponibles_por_dia
    turnos_disponibles_por_dia = {}
    
    for fecha, lista_turnos in turnos_agendados_usuario.items():
        if fecha not in turnos_disponibles_por_dia:
            turnos_disponibles_por_dia[fecha] = {}
            
        for turno in lista_turnos:
            animal = turno["especie"]
            horario = turno["horario"]
            
            if animal not in turnos_disponibles_por_dia[fecha] and animal in db_plantilla_especialistas:
                turnos_disponibles_por_dia[fecha][animal] = db_plantilla_especialistas[animal]["turnos"].copy()
            
            if animal in turnos_disponibles_por_dia[fecha] and horario in turnos_disponibles_por_dia[fecha][animal]:
                turnos_disponibles_por_dia[fecha][animal].remove(horario)

# --- INICIALIZACIÓN DE VARIABLES GLOBALES ---
db_plantilla_especialistas = cargar_base_de_datos()
turnos_agendados_usuario = cargar_turnos_usuarios()
turnos_disponibles_por_dia = {}
sincronizar_disponibilidad_diaria()

# --- FUNCIONES DE CONTROL ---
def mostrar_menu():
    print("\n--- VETERINARIA - MENU PRINCIPAL ---")
    print("1. Ver turnos disponibles de un día")
    print("2. Tomar Turno")
    print("3. Confirmar Turno")
    print("4. Cancelar Turno")
    print("5. Salir")
    return input("Escoge una opción: ").strip()

def desea_continuar():
    """Representa fielmente la actividad y compuerta exclusiva de retorno solicitada"""
    while True:
        rta = input("\n¿Desea realizar otra acción? (S/N): ").strip().upper()
        if rta == 'S' or rta == 'SI': 
            return True
        if rta == 'N' or rta == 'NO': 
            return False
        print("Error: Opción inválida. Ingrese S o N.")

def saludar_y_salir():
    print("\n¡Gracias por comunicarse con nosotros! Que tenga un buen día.")
    exit()

def verificar_fecha_bme(fecha_str):
    try:
        año_actual = datetime.now().year
        fecha_con_año = f"{fecha_str}/{año_actual}"
        datetime.strptime(fecha_con_año, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# --- PROCESOS ---
def ver_turnos():
    print("\n--- [Rama 1] CONSULTAR AGENDA POR DÍA ---")
    fecha = input("Ingrese la fecha a consultar (DD/MM): ").strip()
    if not verificar_fecha_bme(fecha):
        print("Error: Formato de fecha inválido.")
        return False # Cambiado a False para controlar la convergencia

    print(f"\n--- HORARIOS DISPONIBLES PARA EL DÍA {fecha} ---")
    for especie, info in db_plantilla_especialistas.items():
        print(f"\nEspecie: {especie.upper()} -> {info['especialista']}")
        
        if fecha not in turnos_disponibles_por_dia:
            turnos_disponibles_por_dia[fecha] = {}
        if especie not in turnos_disponibles_por_dia[fecha]:
            turnos_disponibles_por_dia[fecha][especie] = info["turnos"].copy()
            
        horarios_libres = turnos_disponibles_por_dia[fecha][especie]
        
        if len(horarios_libres) == 0:
            print("   No quedan horarios disponibles para este día.")
        else:
            for horario in sorted(horarios_libres):
                print(f"   [-] Horario disponible: {horario}hs")
    time.sleep(1)
    return True

def tomar_turno():
    print("\n--- [Rama 2] Tomar Turno ---")
    fecha = input("Ingrese la fecha para el turno (DD/MM): ").strip()
    if not verificar_fecha_bme(fecha):
        print("Error: Formato de fecha inválido.")
        return False  
        
    opciones_validas = ", ".join(db_plantilla_especialistas.keys())
    print(f"Especies en sistema: {opciones_validas}")
    animal = input("Ingresar tipo de animal: ").strip().lower()
    
    if animal not in db_plantilla_especialistas:
        print(f"\nError: No tenemos el personal para atender a un '{animal}'.")
        return False 
        
    especialista = db_plantilla_especialistas[animal]['especialista']
    
    if fecha not in turnos_disponibles_por_dia:
        turnos_disponibles_por_dia[fecha] = {}
    if animal not in turnos_disponibles_por_dia[fecha]:
        turnos_disponibles_por_dia[fecha][animal] = db_plantilla_especialistas[animal]['turnos'].copy()
        
    horarios_libres = turnos_disponibles_por_dia[fecha][animal]
    
    print(f"\nConsultando turnos disponibles para el {fecha}...")
    time.sleep(0.5)
    
    if len(horarios_libres) == 0:
        print(f"Error: No quedan horarios para {animal.upper()} el día {fecha}.")
        return False # Cambiado a False: si falló, no debe intentar guardar en el CSV
        
    horarios_ordenados = sorted(horarios_libres)
    print(f"\nTurnos disponibles ({fecha}):")
    for i, horario in enumerate(horarios_ordenados, start=1):
        print(f"[{i}] {horario}hs")
        
    while True:
        try:
            opcion_turno = int(input("\nEscoger turno (número): "))
            if 1 <= opcion_turno <= len(horarios_ordenados):
                break
            print(f"Error: Opción fuera de rango. Ingrese un número entre 1 y {len(horarios_ordenados)}.")
        except ValueError:
            print("Error: Entrada inválida. Por favor, ingrese un número entero.")

    horario_elegido = horarios_ordenados[opcion_turno - 1]
    
    if fecha in turnos_agendados_usuario:
        for t in turnos_agendados_usuario[fecha]:
            if t['especie'] == animal and t['horario'] == horario_elegido:
                print("Error: Ya tenés agendado un turno idéntico para este animal en este mismo horario.")
                return False

    horarios_libres.remove(horario_elegido)
    
    nuevo_turno = {
        "especie": animal,
        "horario": horario_elegido,
        "estado": "Pendiente",
        "texto": f"Turno para {animal.upper()} a las {horario_elegido}hs con {especialista}"
    }
    if fecha not in turnos_agendados_usuario:
        turnos_agendados_usuario[fecha] = []
    turnos_agendados_usuario[fecha].append(nuevo_turno)
    
    print(f"Agendado turno con éxito para el día {fecha}.")
    return True 

def gestionar_turno_literal(accion_solicitada):
    print(f"\n--- Ingrese la fecha del turno ---")
    fecha = input("Fecha (DD/MM): ").strip()
    
    if not verificar_fecha_bme(fecha):
        print("Error: formato de fecha inválido.")
        return False

    if (fecha not in turnos_agendados_usuario) or (len(turnos_agendados_usuario[fecha]) == 0):
        print(f"\nError: No existe el turno para la fecha {fecha}.")
        return False

    lista_turnos = turnos_agendados_usuario[fecha]
    turno_seleccionado = None
    
    if len(lista_turnos) > 1:
        print(f"\nSe encontraron múltiples turnos para el {fecha}:")
        for idx, t in enumerate(lista_turnos, start=1):
            print(f"   [{idx}] {t['texto']} | Estado: {t['estado']}")
        while True:
            try:
                sel = int(input("Seleccione el turno a gestionar: "))
                if 1 <= sel <= len(lista_turnos):
                    turno_seleccionado = lista_turnos[sel - 1]
                    break
                print(f"Error: Número fuera de rango. Elija entre 1 y {len(lista_turnos)}.")
            except ValueError:
                print("Error: Entrada inválida. Ingrese un número entero.")
    else:
        turno_seleccionado = lista_turnos[0]
        
    print(f"\nBuscando en base de datos... ¡Existe!")
    time.sleep(0.5)
    
    if accion_solicitada == AccionTurno.CANCELAR:
        animal = turno_seleccionado['especie']
        horario = turno_seleccionado['horario']
        
        if fecha in turnos_disponibles_por_dia and animal in turnos_disponibles_por_dia[fecha]:
            if horario not in turnos_disponibles_por_dia[fecha][animal]:
                turnos_disponibles_por_dia[fecha][animal].append(horario)
                
        lista_turnos.remove(turno_seleccionado)
        if len(lista_turnos) == 0:
            turnos_agendados_usuario.pop(fecha)
            
        print("Turno cancelado exitosamente.")
        return True 
    else:
        turno_seleccionado['estado'] = "CONFIRMADO"
        print(f"\n   Turno: {turno_seleccionado['texto']}")
        print(f"   Estado: {turno_seleccionado['estado']}")
        return True 

# --- FLUJO PRINCIPAL UNIFICADO (Alineado con Eduardo y BPMN) ---
def main():
    while True:
        opcion = mostrar_menu()
        exito_operacion = False # Bandera para saber si confluimos a la pregunta final
        
        if opcion == OpcionesMenu.VER_TURNOS.value:
            exito_operacion = ver_turnos()
            
        elif opcion == OpcionesMenu.TOMAR_TURNO.value:
            if tomar_turno():
                guardar_turnos_usuarios()
                exito_operacion = True
                
        elif opcion == OpcionesMenu.CONFIRMAR_TURNO.value:
            if gestionar_turno_literal(AccionTurno.CONFIRMAR):
                guardar_turnos_usuarios()
                exito_operacion = True
                
        elif opcion == OpcionesMenu.CANCELAR_TURNO.value:
            if gestionar_turno_literal(AccionTurno.CANCELAR):
                guardar_turnos_usuarios()
                exito_operacion = True
                
        elif opcion == OpcionesMenu.SALIR.value:
            saludar_y_salir()
            
        else:
            print("Error: Opción Inválida.")
            time.sleep(1)
            continue # Si erró la opción, vuelve a mostrar el menú directo sin preguntar

        # -------------------------------------------------------------
        # COMPUERTA DE CONVERGENCIA ÚNICA 
        # -------------------------------------------------------------
        # Si la operación fue exitosa (o se completó la consulta de la rama 1),
        # todos los flujos confluyen estrictamente en este punto del código:
        if exito_operacion:
            if not desea_continuar():
                saludar_y_salir()
        else:
            # Si hubo un error de validación interna, el sistema da un respiro y vuelve al menú
            time.sleep(1)

if __name__ == "__main__":
    main()