# VetCare - Sistema Automatizado de Gestión de Turnos

VetCare es una aplicación de consola desarrollada en Python que simula un asistente virtual interactivo (chatbot) para la autogestión de citas veterinarias.

El proyecto surge como el Trabajo Práctico Integrador (TPI) para la materia **Organización Empresarial** de la **Tecnicatura Universitaria en Programación (UTN)**, con el objetivo de modelar y automatizar un proceso de negocio que previamente presentaba ineficiencias en su gestión manual.

---

## 🎯 Problemática Detectada & Solución

### Proceso Manual (As-Is)

Durante el análisis del proceso tradicional operado por una recepcionista, se identificaron cuellos de botella críticos: riesgo de solapamiento de turnos por errores humanos, saturación de canales de atención, demoras administrativas y dependencia estricta del horario comercial.

### Proceso Automatizado (To-Be)

Se diseñó e implementó un chatbot que automatiza el ciclo de vida de las reservas, reduciendo las tareas repetitivas y garantizando la disponibilidad del servicio las 24 horas. El modelado de ambos estados se realizó utilizando el estándar **BPMN 2.0**.

---

## 🛠️ Características Técnicas Principales

- **Arquitectura Resiliente:** Implementa una máquina de estados simplificada para administrar el flujo del turno.
- **Tipado Estricto con Enums:** Centralización de las opciones del menú y los estados de las citas (`Pendiente` y `Confirmado`) mediante la clase `Enum` de Python, garantizando consistencia semántica.
- **Persistencia y Contingencia (CSV):** El sistema lee dinámicamente un archivo estructurado `especialistas.csv`. Si este no existe, presenta errores de formato o está vacío, activa automáticamente un mecanismo de respaldo precargando los datos en memoria.
- **Control de "Caminos Infelices":** Manejo robusto de excepciones para mitigar ingresos erróneos:
  - Validación de formatos de fecha `DD/MM` sincronizados con el año en curso.
  - Exclusión dinámica de franjas horarias previamente reservadas (evita solapamientos).
  - Control ante ingresos de texto en menús numéricos y desbordamiento de rangos.

---

## ⚙️ Estructura de la Base de Datos (`especialistas.csv`)

Para la carga externa de profesionales, el sistema requiere un archivo CSV en la raíz del proyecto estructurado con cabeceras específicas. Las franjas horarias se delimitan mediante puntos y comas:

```csv
animal, especialista, turnos
perro, Dr. Perez (Caninos), 10:00;14:00
gato, Dra. Martinez (Felinos), 11:00;16:00
ave, Dr. Silva (Aves), 09:30;15:00
```

---

## 🚀 Funcionalidades

1. Ver turnos disponibles: Consulta en tiempo real las agendas libres por fecha, descontando dinámicamente las citas tomadas.
1. Tomar Turno: Flujo guiado que valida la especie y despliega un menú incremental con horarios libres para reservar en estado Pendiente.
1. Confirmar Turno: Transiciona el ciclo de vida del turno seleccionado de Pendiente a Confirmado.
1. Cancelar Turno: Elimina la cita de la colección activa, liberando la franja horaria de inmediato.
1. Salir: Finaliza la ejecución limpiando las estructuras temporales en memoria.

---

📦 Ejecución y Requisitos

- Python 3.8 o superior.

```bash
# Clonar el repositorio
git clone https://github.com/GastonUFernandez/TPI-Veterinaria-Python.git

# Ingresar al directorio
cd TPI-Veterinaria-Python

# Ejecutar el programa
python main.py
```

---

## 👥 Autores & Contexto Académico

- Gastón Uriel Fernández
- Mirko Alexander Stamm

**Universidad Tecnológica Nacional** (UTN) Tecnicatura Universitaria en Programación

Materia: _Organización Empresarial_ | Año Lectivo 2026
