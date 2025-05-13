# 🏥 Práctica de Concurrencia y Paralelismo: Simulación de un Sistema Hospitalario

**Universidad Nacional Autónoma de México**  

**Facultad de Estudios Superiores Acatlán**

**Licenciatura en Matemáticas Aplicadas y Computación** 

**Asignatura: Programación Paralela y Concurrente**  

**Profesor: José Gustavo Fuentes Cabrera**  

**Fecha de entrega: 04/05/2025**  

**Alumno: Ramírez Gómez Fernando Axel** 

**Número de cuenta: 422066442**

![image](https://github.com/user-attachments/assets/a94d6edc-5187-4b19-8beb-0b8ab05333cd)
---

## 📘 Descripción general

Este proyecto presenta una simulación de un sistema hospitalario que incorpora los paradigmas de programación **paralela**, **concurrente** y **asíncrona** mediante Python. El sistema permite modelar el paso de pacientes por distintas etapas clínicas: registro, triaje asistido por IA, diagnóstico automatizado, asignación de camas y seguimiento, todo bajo un control centralizado y asincrónico.

![image](https://github.com/user-attachments/assets/f78f8e4e-255d-4641-acc6-7ea3fea0b2e0)
---

## 🎯 Objetivo

Aplicar y diferenciar los paradigmas de programación paralela, concurrente y asíncrona a través del desarrollo de una simulación hospitalaria que exija la ejecución distribuida de tareas dependientes del tiempo y los recursos disponibles.

---

## 🧠 Introducción

El sistema simula un hospital virtual donde los pacientes presentan síntomas aleatorios, son clasificados según su urgencia y reciben un diagnóstico clínico automatizado. Se implementa una arquitectura modular en Python, donde cada componente representa una fase del flujo hospitalario.  

Se integran herramientas como:

- `asyncio` para operaciones I/O bound sin bloqueo.
- `scikit-learn` para modelos predictivos de triaje y diagnóstico.
- `ProcessPoolExecutor` para ejecución de tareas CPU bound en paralelo.
- `joblib` para persistencia de modelos.
- `asyncio.Semaphore` para gestionar recursos limitados (camas).

---

## 📁 Estructura del proyecto

```plaintext
Hospital_Sim/                              # Directorio raíz del proyecto
│
├── Hospital_Sim/                          # Carpeta principal con el código fuente
│   │
│   ├── main.py                            # Punto de entrada que coordina la simulación completa
│   ├── paciente.py                        # Define la estructura y atributos del paciente
│   ├── registro.py                        # Gestiona el ingreso de pacientes al sistema
│   ├── triage_ia.py                       # Clasifica pacientes por prioridad usando IA
│   ├── diagnostico_ia.py                 # Realiza diagnóstico médico automatizado con IA
│   ├── asignacion_recursos.py            # Simula la asignación de recursos hospitalarios
│   ├── seguimiento.py                     # Registra la evolución y estado del paciente
│   ├── visualizacion.py                   # Muestra estadísticas y visualizaciones del sistema
│   ├── modelo_entrenamiento.py           # Permite entrenar modelos para diagnóstico y triage
│   │
│   ├── modelo_diagnostico.pkl            # Modelo de IA entrenado para diagnóstico
│   ├── modelo_triage.pkl                 # Modelo de IA entrenado para clasificación por prioridad
│   ├── label_enfermedad.pkl              # Etiquetas usadas en el modelo de diagnóstico
│   ├── label_prioridad.pkl               # Etiquetas usadas en el modelo de triage

```
---
## ⚙️ ¿Cómo se ejecuta?

Asegúrate de tener **Python 3.10+** instalado en tu sistema.

Instala las dependencias necesarias con:

```bash
pip install -r requirements.txt
```
Luego ejecuta la simulación con:

```bash
python Hospital_Sim/main.py
```
## 🧱 Diseño y patrones aplicados
Para asegurar claridad, eficiencia y escalabilidad, se emplearon diversos patrones de diseño:

* **Factory:** Generación dinámica de pacientes con síntomas aleatorios.
* **Singleton:** Logger centralizado para mantener la consistencia en el formato de salida.
* **Semáforo (`asyncio.Semaphore`):** Control del acceso a camas disponibles, evitando condiciones de carrera.
* **Pipeline asincrónico:** Orquestación secuencial de cada etapa clínica del flujo hospitalario.

## 🧠 Relación con los paradigmas
Este proyecto incorpora múltiples enfoques computacionales:

* **Asincronía:** Utilizada en tareas dependientes de I/O, como el registro y el seguimiento del paciente.
* **Paralelismo:** Aplicado a operaciones intensivas en CPU, como la inferencia de modelos de Machine Learning.
* **Orientación a objetos (OOP):** Presente en el diseño de clases como `Paciente`, que encapsulan datos y comportamiento.
* **Estilo funcional:** Utilizado en módulos sin estado ni efectos colaterales, como `triage_ia.py`.

## 🧪 Pruebas y resultados
Se ejecutaron simulaciones con diferentes volúmenes de pacientes: 4, 10 y 30. En todos los escenarios:

* El sistema respondió de forma estable y fluida.
* La asignación de camas fue eficiente, respetando la disponibilidad limitada.
* La clasificación de pacientes fue precisa, basada en los modelos ML previamente entrenados.
* Las salidas del sistema reflejan correctamente el avance del paciente por cada etapa del flujo hospitalario.

## ✅ Conclusión
Este proyecto demuestra cómo los paradigmas de programación concurrente, paralela y asíncrona pueden aplicarse eficazmente para modelar un sistema hospitalario complejo y realista.
La arquitectura propuesta es:

* **Extensible:** Permite integrar nuevos módulos, como historia clínica o chatbot médico.
* **Robusta:** Maneja adecuadamente los recursos limitados y múltiples tareas simultáneas.
* **Didáctica:** Útil como referencia para enseñar conceptos clave de programación moderna.

## 🤖 Consideraciones sobre el uso de herramientas de IA

- DeepMind. (2018). Investigación en IA para la salud y aplicaciones clínicas [Iniciativas en colaboración con sistemas de salud].
- Google. (2024). Gemini [Modelo de IA avanzada para aplicaciones en el dominio médico].

Durante el desarrollo de este proyecto se utilizó una herramienta de Inteligencia Artificial como apoyo para:

* Estructuración y revisión técnica del código.
* Mejora de redacción en la documentación.
* Generación de ideas para el diseño del sistema.
