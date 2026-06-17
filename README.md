# VetCare - Sistema Automatizado de Gestión de Turnos

## Descripción

VetCare es una simulación de un asistente virtual (chatbot) desarrollado en Python para la gestión de turnos en una clínica veterinaria.

El proyecto surge como parte del Trabajo Práctico Integrador (TPI) de la materia **Organización Empresarial** de la **Tecnicatura Universitaria en Programación (UTN)**, con el objetivo de modelar y automatizar un proceso de negocio previamente realizado de forma manual.

La solución permite a los usuarios consultar disponibilidad, reservar turnos, confirmar citas y gestionar cancelaciones mediante una interfaz de consola.

---

## Problemática Detectada

Durante el análisis del proceso actual se identificaron las siguientes ineficiencias:

- Riesgo de solapamiento de turnos por errores manuales.
- Saturación de los canales de atención.
- Demoras en la gestión administrativa.
- Dependencia del horario comercial para realizar reservas o cancelaciones.

---

## Solución Propuesta

Se desarrolló un chatbot que automatiza el proceso de gestión de turnos veterinarios mediante:

- Consulta de disponibilidad.
- Reserva de turnos.
- Confirmación de citas.
- Cancelación de reservas.
- Validación de entradas y manejo de errores.

La automatización reduce tareas administrativas repetitivas y mejora la organización de la agenda de especialistas.

---

## Funcionalidades

- Ver turnos disponibles por fecha.
- Reservar un turno para una especie determinada.
- Confirmar reservas existentes.
- Cancelar turnos.
- Validación de datos ingresados por el usuario.
- Manejo de casos de error ("camino infeliz").

---

## Modelado del Proceso

El sistema fue diseñado utilizando BPMN 2.0 mediante dos modelos:

### As-Is

Representa el proceso manual realizado por la recepcionista.

### To-Be

Representa el proceso automatizado mediante el chatbot.

---

## Tecnologías Utilizadas

- Python 3
- CSV para persistencia de datos
- BPMN 2.0 para modelado de procesos
- Git
- GitHub

---

## Ejecución

Clonar el repositorio:

```bash
git clone https://github.com/GastonUFernandez/TPI-Veterinaria-Python.git
```

Ingresar al directorio:

```bash
cd TPI-Veterinaria-Python
```

Ejecutar el programa:

```bash
python TPI_OE_Fernandez_Gaston_Uriel_Stamm_Mirko_Alexander.py
```

---

## Autores

- Gastón Uriel Fernández
- Mirko Alexander Stamm

---

## Materia

**Organización Empresarial**
Tecnicatura Universitaria en Programación
Universidad Tecnológica Nacional (UTN)
Año Lectivo 2026
