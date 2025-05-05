# Práctica de concurrencia y paralelismo

**Universidad Nacional Autónoma de México**

**Facultad de Estudios Superiores Acatlán**

**Licenciatura en Matemáticas Aplicadas y Computación**

**Programación Paralela y Concurrente**

Prof. José Gustavo Fuentes Cabrera

04/05/2025

**Alumno:** Ramírez Gómez Fernando Axel

**No. C.** 422066442

![image](https://github.com/user-attachments/assets/a94d6edc-5187-4b19-8beb-0b8ab05333cd)


# Práctica de Concurrencia y Paralelismo: Simulación de un Sistema Hospitalario

Este repositorio contiene el código y la documentación de una simulación de un sistema hospitalario utilizando paradigmas de programación paralela, concurrente y asíncrona en Python.
![image](https://github.com/user-attachments/assets/f78f8e4e-255d-4641-acc6-7ea3fea0b2e0)


## Objetivo

Aplicar y diferenciar los paradigmas de programación paralela, concurrente y asíncrona mediante la simulación de un sistema realista que requiere procesamiento distribuido de tareas en distintos tiempos y recursos.

## Introducción

El proyecto simula un hospital virtual donde los pacientes son entidades con síntomas dinámicos, prioridades cambiantes y recursos limitados. Se ha construido un ecosistema en Python que abarca desde el registro de un paciente hasta su alta, incluyendo triaje automatizado con IA, diagnóstico predictivo y una gestión asincrónica de recursos limitados como las camas.

Se utilizaron herramientas como `asyncio` para la gestión de colas no bloqueantes, `scikit-learn` para la predicción de enfermedades y formateadores de logs personalizados. El desarrollo implicó superar desafíos de concurrencia, problemas con modelos de IA y gestión de recursos compartidos. Este README documenta los retos técnicos, las soluciones implementadas y la estructura del sistema.

## Diagrama del Sistema

El sistema se estructura modularmente para simular el flujo de un paciente a través de diferentes etapas hospitalarias. Un diagrama de flujo técnico ilustra las interacciones entre los módulos de Registro, Triage IA, Diagnóstico IA, Modelo de Entrenamiento, Asignación de Camas y Seguimiento, orquestados por el módulo principal (`Main.py`).

## Diseño Detallado

Se aplicaron diversos patrones de diseño para estructurar el sistema:

* **Factory:** Para la creación flexible de pacientes con síntomas.
* **Singleton:** Para garantizar una única instancia del logger con configuración consistente.
* **Semáforo:** Para el control concurrente de recursos limitados (camas) con `asyncio.Semaphore`.
* **Pipeline:** Para la orquestación secuencial de etapas clínicas asíncronas.

La estructura modular del proyecto asigna responsabilidades claras a cada componente:

* `main.py`: Controlador central del flujo asíncrono.
* `registro.py`: Módulo de I/O bound (simula bases de datos).
* `triage_ia.py`/`diagnostico_ia.py`: Módulos CPU bound (inferencia con modelos ML).
* `asignacion_recursos.py`: Gestión asíncrona de recursos críticos.
* `visualizacion.py`: Configuración de logs y estadísticas.
* `paciente.py`: Entidad central con lógica de generación de datos.

## Librerías Clave

* `asyncio`: Para concurrencia en operaciones I/O bound.
* `joblib`: Para serialización eficiente de modelos ML.
* `sklearn`: Para entrenamiento y predicción con modelos de Machine Learning (Decision Tree Classifier).
* `pandas`: Para transformación de datos en la etapa de diagnóstico.

## Desafíos Técnicos y Soluciones

1.  **Sincronización de Recursos:** Se resolvió la contienda por camas utilizando semáforos asíncronos (`asyncio.Semaphore`).
2.  **Integración de Modelos ML en Entorno Asíncrono:** Para evitar que la inferencia bloqueante (CPU bound) detuviera el event loop asíncrono, se utilizó `ProcessPoolExecutor` para ejecutar los modelos en paralelo.
3.  **Consistencia de Logs:** Se implementó un patrón Singleton para el formateador de logs (`ColoredFormatter`) asegurando una configuración centralizada y consistente.

## Código Clave Explicado

El corazón de la simulación reside en la función asíncrona `flujo_paciente_async` en `main.py`, que orquesta las diferentes etapas del proceso hospitalario utilizando `await` para tareas asíncronas y `await loop.run_in_executor` para ejecutar tareas síncronas intensivas en CPU en un `ProcessPoolExecutor`.

La simulación de recursos limitados, como las camas, se maneja en `asignacion_recursos.py` utilizando `asyncio.Semaphore`. La integración de modelos ML para triaje y diagnóstico se realiza ejecutando las funciones síncronas de inferencia dentro del `ProcessPoolExecutor` para no bloquear el bucle de eventos principal.

Se realizó una modificación en la lógica de seguimiento (`seguimiento.py`) para asegurar que los pacientes que inicialmente requieren observación eventualmente transiten al estado de alta médica después de un período simulado.

## Relación con la Arquitectura

La implementación demuestra la aplicación de:

* **AsyncIO:** Para manejar eficientemente operaciones I/O bound de forma concurrente.
* **OOP:** En la encapsulación de la lógica en clases como `Paciente` y los modelos ML.
* **Funcional:** En módulos como `triage_ia.py` que evitan efectos secundarios.
* **Concurrencia y Paralelismo:** Mediante el uso de semáforos para recursos compartidos y `ProcessPoolExecutor` para tareas CPU bound.

## Pruebas y Rendimiento

Se realizaron simulaciones con diferentes cantidades de pacientes (4, 10, 30) para observar el comportamiento del sistema. La salida detallada de la simulación con 4 pacientes demuestra la ejecución concurrente de las etapas y la correcta aplicación de la lógica de alta tras observación. Las estadísticas finales confirman el progreso de los pacientes a través del flujo sin errores en los escenarios simulados. El tiempo total de simulación varía según la cantidad de pacientes y valida la simulación de tiempos de espera y observación.

## Conclusión

La simulación demuestra eficazmente el uso de herramientas de concurrencia en Python (`asyncio`, `ProcessPoolExecutor`) para modelar un sistema complejo con diferentes tipos de tareas y recursos limitados. La integración de modelos de ML se realiza sin degradar el rendimiento del bucle principal. La flexibilidad del modelo permite analizar el impacto de los recursos en el flujo de pacientes bajo diferentes escenarios.

## Uso Ético y Documentado de IA

Durante el desarrollo de esta práctica, se utilizó una Inteligencia Artificial como herramienta auxiliar para diversos fines, siempre de forma ética y documentada.
