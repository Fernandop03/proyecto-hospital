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

## Índice

* Objetivo
* Introducción 
* Diagrama del Sistema
* Diseño Detallado 
* Estructura Modular 
* Código Clave Explicado
* Relación con la Arquitectura 
* Pruebas y Rendimiento 
* Conclusión 
* Referencias 

## Objetivo

Aplicar y diferenciar los paradigmas de programación paralela, concurrente y asíncrona mediante la simulación de un sistema realista que requiere procesamiento distribuido de tareas en distintos tiempos y recursos.

## Introducción

Este proyecto desarrolla un hospital virtual donde los pacientes son entidades dinámicas con síntomas cambiantes, prioridades variables y recursos limitados. Creamos un ecosistema en Python que simula el flujo completo de un paciente, desde el registro hasta el alta. Esto incluye triaje automatizado con IA, diagnóstico predictivo y la gestión asíncrona de recursos limitados como las camas (simulando solo 3 por motivos académicos).

Utilizamos herramientas como `asyncio` para gestionar colas sin bloquear el sistema, `scikit-learn` para predecir enfermedades basadas en síntomas aleatorios y logs formateados con `ColoredFormatter` para una visualización clara. Durante el desarrollo, enfrentamos desafíos como errores de concurrencia, modelos de ML que no generalizaban adecuadamente y un deadlock en el semáforo de camas.

Este informe detalla los retos técnicos, las soluciones implementadas (y descartadas) y cómo logramos la armonía del sistema. Cada línea de código, desde el `Semaphore` que controla las camas hasta el `LabelEncoder` que traduce diagnósticos, tiene un propósito. Aunque no es perfecto, es nuestra implementación, documentada para facilitar futuras iteraciones.

![image](https://github.com/user-attachments/assets/6ca496cb-9c85-4709-8e62-d9ebdfdf64af)

## Diagrama del Sistema

El siguiente diagrama ilustra el flujo general del sistema simulado:

![image](https://github.com/user-attachments/assets/86df84af-c077-474c-b548-f026b770e35f)

*(Referencia: Imagen generada por inteligencia artificial con ChatGPT de OpenAI, 2025. Diagrama de flujo técnico de un sistema hospitalario simulado. Creado el 30 de abril de 2025 mediante prompt personalizado)*

## Diseño Detallado

### Patrones de Diseño Aplicados

Exploramos y aplicamos diversos patrones de diseño para estructurar el simulador:

| Patrón     | Módulo/Clase              | Propósito                                                                    | Implementación Clave                                                                   |
| :--------- | :------------------------ | :--------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| Factory    | `Paciente`                | Creación flexible de pacientes con síntomas aleatorios o predefinidos.       | Función `generar_sintomas()` encapsula la lógica de construcción.                    |
| Singleton  | `ColoredFormatter`        | Garantizar una única instancia del logger con configuración consistente.       | Configuración centralizada en `main.py`.                                             |
| Semáforo   | `asignacion_recursos.py`  | Control concurrente de acceso a recursos limitados (camas) usando `asyncio`. | Uso de `asyncio.Semaphore(3)` para limitar el acceso a 3.                            |
| Pipeline   | `flujo_paciente_async()`  | Orquestación secuencial de las etapas clínicas del paciente (Registro, Triage, Diagnóstico, Cama, Seguimiento). | Encadenamiento de tareas asíncronas mediante `await`.                                  |

### Estructura Modular

La arquitectura se basa en la separación de responsabilidades en módulos claros:

* `main.py`: Actúa como controlador central, coordinando el flujo asíncrono de los pacientes.
* **Módulos Clínicos:**
    * `registro.py`: Simula operaciones I/O bound (bases de datos).
    * `triage_ia.py`/`diagnostico_ia.py`: Contienen la lógica CPU bound para la inferencia con modelos de Machine Learning.
    * `asignacion_recursos.py`: Gestiona de forma asíncrona recursos críticos como las camas.
* **Módulos Utilitarios (`Utils`):**
    * `visualizacion.py`: Configura los logs y maneja la presentación de estadísticas.
    * `paciente.py`: Define la entidad central del sistema (`Paciente`) y su lógica de generación de datos.

### Librerías Clave

Las siguientes librerías fueron fundamentales para el desarrollo:

| Librería  | Uso Principal                                                                 | Ejemplo Aplicado                                            |
| :-------- | :---------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `asyncio` | Gestión de concurrencia para operaciones I/O bound (registro, asignación de camas). | Implementación de `async def asignar_cama_async()`.        |
| `joblib`  | Serialización eficiente de modelos ML para una carga e inferencia rápidas.      | Uso de `joblib.load()` en `triage_ia.py`.                   |
| `sklearn` | Entrenamiento y predicción con modelos (ej. Decision Tree Classifier).          | Uso de Pipeline para el procesamiento en `modelo_entrenamiento.py`. |
| `pandas`  | Transformación y manipulación de datos para el diagnóstico (DataFrames).      | Integrado en el Pipeline de `modelo_entrenamiento.py`.    |

### Desafíos Técnicos y Soluciones

Durante el desarrollo, abordamos los siguientes desafíos:

1.  **Sincronización de Recursos:**
    * **Problema:** Múltiples pacientes concurrentes compitiendo por un número limitado de camas.
    * **Solución:** Implementación de semáforos asíncronos (`asyncio.Semaphore`) para garantizar la exclusión mutua y controlar el acceso a las camas.

2.  **Integración de Modelos ML en Entorno Asíncrono:**
    * **Problema:** Las operaciones de inferencia de los modelos de ML son CPU bound y podían bloquear el bucle de eventos asíncrono.
    * **Solución:** Ejecución de las tareas de inferencia en un `ProcessPoolExecutor` para procesarlas en paralelo en procesos separados, evitando así el bloqueo del bucle principal.

3.  **Consistencia de Logs:**
    * **Problema:** Necesidad de un formato centralizado para los logs, incluyendo colores y emojis, para una mejor visualización.
    * **Solución:** Aplicación del patrón Singleton en el `ColoredFormatter` para asegurar una configuración única y consistente del sistema de logging a través de `logging.getLogger(__name__)`.

## Diagrama de Secuencia (Ejemplo: Flujo de un Paciente)

El diagrama de secuencia ilustra el recorrido típico de un paciente a través del sistema:

![image](https://github.com/user-attachments/assets/7db7fa6b-15dd-4aa9-9c44-c0e2649e3d80)

Este diseño se optimiza para:
* **Escalabilidad:** La modularidad permite añadir fácilmente nuevas funcionalidades (ej. módulo de facturación).
* **Mantenibilidad:** La aplicación de patrones de diseño y la separación de responsabilidades facilitan las modificaciones.
* **Rendimiento:** `AsyncIO` se encarga de las operaciones I/O, mientras que el multiprocesamiento maneja las tareas CPU bound.

## Código Clave Explicado

A continuación, se detallan algunos fragmentos de código fundamentales para la simulación:

Este informe documenta el desarrollo y la ejecución de una simulación del flujo de pacientes en un entorno hospitalario. La simulación utiliza programación asíncrona (`asyncio`), procesamiento paralelo (`ProcessPoolExecutor`) y modelos de aprendizaje automático para etapas como registro, triaje, diagnóstico, asignación de recursos (camas) y seguimiento. El objetivo es modelar y analizar el rendimiento del sistema bajo diferentes condiciones.

1.  **Orquestación del Flujo del Paciente (`main.py`)**

    La función `flujo_paciente_async` es central para la simulación de cada paciente. Define la secuencia de etapas por las que transita un paciente y orquesta el proceso hospitalario de forma asíncrona.

    ```python
    # main.py
    import logging
    import asyncio
    from concurrent.futures import ProcessPoolExecutor

    # Assuming logger and actualizar_estadistica_global are defined elsewhere
    logger = logging.getLogger(__name__)

    async def flujo_paciente_async(paciente, cpu_executor: ProcessPoolExecutor, actualizar_estadistica_global):
        logger.info(f"Paciente {paciente.id} [SIMULACION]: Iniciando flujo...")
        try:
            # 1. Registro (I/O bound simulado)
            await registrar_paciente_async(paciente, actualizar_estadistica_global)
            if paciente.estado == "error_registro" or paciente.estado == "registro_cancelado":
                logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo detenido debido a {paciente.estado}.")
                return

            # 2. Triage (CPU bound - ejecutado en ProcessPoolExecutor)
            logger.info(f"Paciente {paciente.id} [TRIAGE]: Iniciando triaje...")
            loop = asyncio.get_running_loop()
            try:
                # Assuming clasificar_prioridad is a sync function defined elsewhere
                paciente.prioridad = await loop.run_in_executor(
                    cpu_executor, clasificar_prioridad, paciente.sintomas
                )
                logger.info(f"Paciente {paciente.id} [TRIAGE]: Prioridad {paciente.prioridad}")
                await actualizar_estadistica_global('triage')
            except Exception as e:
                logger.error(f"Paciente {paciente.id} [ERROR TRIAGE]: Error en triaje: {type(e).__name__} - {e}", exc_info=True)
                paciente.estado = "error_triage"
                await actualizar_estadistica_global('error_triage')
                logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo detenido debido a error en triaje.")
                return

            # 3. Diagnóstico (CPU bound - ejecutado en ProcessPoolExecutor)
            logger.info(f"Paciente {paciente.id} [DIAGNOSTICO]: Iniciando diagnóstico...")
            try:
                 # Assuming diagnosticar_paciente_sincrono is a sync function defined elsewhere
                paciente = await loop.run_in_executor(
                    cpu_executor, diagnosticar_paciente_sincrono, paciente
                )
                if paciente.estado == "diagnosticado":
                    await actualizar_estadistica_global('diagnostico')
                #... (manejo de estado y errores)
            except Exception as e:
                logger.error(f"Paciente {paciente.id} [ERROR DIAGNOSTICO]: Error en diagnóstico: {type(e).__name__} - {e}", exc_info=True)
                paciente.estado = "error_diagnostico"
                await actualizar_estadistica_global('error_diagnostico')


            # 4. Asignación de Cama y Tratamiento (Recurso limitado con asyncio.Semaphore)
            recibio_cama = False
            if paciente.estado not in ["error_registro", "error_triage", "flujo_cancelado", "error_diagnostico"]: # Added error_diagnostico to check
                try:
                    recibio_cama = await asignar_cama_async(paciente, actualizar_estadistica_global)
                except Exception as e:
                    logger.error(f"Paciente {paciente.id} [ERROR CAMA]: Error en asignación de cama: {type(e).__name__} - {e}", exc_info=True)
                    paciente.estado = "error_cama"
                    await actualizar_estadistica_global('error_cama')
                    recibio_cama = False


            # 5. Seguimiento (I/O bound simulado)
            if paciente.estado not in ["alta", "error_registro", "error_triage", "flujo_cancelado", "cama_cancelada", "error_cama", "error_ejecutor_cama", "error_diagnostico", "tratamiento_completado"]: # Added relevant states
                logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Iniciando etapa de seguimiento...")
                try:
                    await seguimiento_paciente(paciente, actualizar_estadistica_global, recibio_cama)
                except Exception as e:
                    logger.error(f"Paciente {paciente.id} [ERROR SEGUIMIENTO]: Error en seguimiento: {type(e).__name__} - {e}", exc_info=True)
                    paciente.estado = "error_seguimiento"
                    await actualizar_estadistica_global('error_seguimiento')


            # 6. Finalización del Flujo del Paciente
            logger.info(f"Paciente {paciente.id} [SIMULACION]: Flujo finalizado con estado '{paciente.estado}'.")


        except asyncio.CancelledError:
            logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo cancelado.")
            paciente.estado = "flujo_cancelado"
            await actualizar_estadistica_global('flujo_cancelado')


        except Exception as e:
            logger.error(f"Paciente {paciente.id} [SIMULACION]: Error desconocido en el flujo: {type(e).__name__} - {e}", exc_info=True)
            paciente.estado = "error_desconocido"
            await actualizar_estadistica_global('error_desconocido')

    # Assuming registrar_paciente_async, clasificar_prioridad, diagnosticar_paciente_sincrono, asignar_cama_async, and seguimiento_paciente are defined elsewhere
    ```
    **Explicación:** Esta función define el camino asíncrono de cada paciente. Utiliza `await` para esperar tareas asíncronas (registro, cama, seguimiento) y `await loop.run_in_executor` para ejecutar tareas síncronas CPU bound (triage, diagnóstico) en un `ProcessPoolExecutor`, evitando bloquear el bucle de eventos principal.

2.  **Simulación de Recurso Limitado (Camas - `asignacion_recursos.py`)**

    La función `asignar_cama_async` ilustra cómo simular un recurso limitado (camas) utilizando un semáforo asíncrono:

    ```python
    # asignacion_recursos.py
    import logging
    import asyncio
    import random

    logger = logging.getLogger(__name__)

    camas_disponibles = asyncio.Semaphore(3)

    async def asignar_cama_async(paciente, actualizar_estadisticas_func):
        logger.info(f"Paciente {paciente.id} [CAMA]: Esperando cama disponible...")
        try:
            # Intentar adquirir el semáforo asincrono
            async with camas_disponibles:
                logger.info(f"Paciente {paciente.id} [CAMA]: Cama asignada - Iniciando tratamiento")
                # Registrar cama asignada
                await actualizar_estadisticas_func('cama_asignada')

                # Simular tiempo de tratamiento
                tiempo_tratamiento = random.uniform(2, 5)
                await asyncio.sleep(tiempo_tratamiento) # Usar await asyncio.sleep

                logger.info(f"Paciente {paciente.id} [TRATAMIENTO]: Tratamiento completado en {tiempo_tratamiento:.1f}s")
                paciente.estado = "tratamiento_completado" # Nuevo estado para indicar fin del tratamiento
                return True # Indica que recibió cama
        except Exception as e:
            # ... (manejo de errores)
            logger.error(f"Paciente {paciente.id} [ERROR CAMA]: Error en asignación de cama: {type(e).__name__} - {e}", exc_info=True)
            paciente.estado = "error_cama"
            await actualizar_estadisticas_func('error_cama')
            return False
    ```
    **Explicación:** `asyncio.Semaphore(3)` crea un semáforo con 3 permisos iniciales (representando 3 camas). `async with camas_disponibles:` intenta adquirir un permiso. Si hay permisos disponibles, se adquiere instantáneamente y el contador disminuye. Si no, la tarea espera hasta que se libere un permiso.

3.  **Integración de Modelos ML (Triage - `main.py` y `triage_ia.py`)**

    La simulación incorpora modelos pre-entrenados para triaje y diagnóstico. Su ejecución se realiza en un `ProcessPoolExecutor` para evitar bloquear el bucle de eventos principal, ya que son tareas intensivas en CPU.

    ```python
    # main.py snippet (part of flujo_paciente_async)
    # 2. Triage (CPU rapido)
    logger.info(f"Paciente {paciente.id} [TRIAGE]: Iniciando triaje...")
    loop = asyncio.get_running_loop()
    try:
        # Assuming clasificar_prioridad is defined in triage_ia.py and imported
        paciente.prioridad = await loop.run_in_executor(
            cpu_executor, clasificar_prioridad, paciente.sintomas
        )
        logger.info(f"Paciente {paciente.id} [TRIAGE]: Prioridad {paciente.prioridad}")
        await actualizar_estadistica_global('triage')
    except Exception as e:
        logger.error(f"Paciente {paciente.id} [ERROR TRIAGE]: Error en triaje: {type(e).__name__} - {e}", exc_info=True)
        paciente.estado = "error_triage"
        await actualizar_estadistica_global('error_triage')
        logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo detenido debido a error en triaje.")
        return

    # triage_ia.py snippet
    def clasificar_prioridad(sintomas_dict):
        sintomas = [
            sintomas_dict.get("fiebre", 0),
            sintomas_dict.get("tos", 0),
            sintomas_dict.get("dolor", 0),
            sintomas_dict.get("fatiga", 0),
            sintomas_dict.get("respirar", 0),
        ]
        # ... (modelo loading and prediction logic)
        # return predicted_priority
    ```
    **Explicación:** `triage_ia.py` contiene la función síncrona `clasificar_prioridad`. En `main.py`, `await loop.run_in_executor` envía esta función y sus argumentos a un `ProcessPoolExecutor`, permitiendo que la tarea intensiva en CPU se ejecute en otro proceso sin bloquear el bucle principal de `asyncio`.

4.  **Lógica de Seguimiento y Alta (Modificada - `seguimiento.py`)**

    Para asegurar que los pacientes bajo observación eventualmente reciban el alta, modificamos la lógica de la etapa "requiere_observacion":

    ```python
    # seguimiento.py
    import logging
    import asyncio
    import random

    logger = logging.getLogger(__name__)

    async def seguimiento_paciente(paciente, actualizar_estadisticas_func, recibio_cama=False):
        if paciente.estado in ['alta', 'error_registro', 'error_diagnostico', 'error_cama', 'seguimiento_cancelado', 'error_seguimiento']: # Added error_seguimiento
            return

        logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Iniciando seguimiento...")

        try:
            # Simular latencia de red
            tiempo_latencia = random.uniform(1, 3)
            await asyncio.sleep(tiempo_latencia)

            resultados = ["estable", "mejorando", "requiere_observacion"]
            pesos = [0.4, 0.4, 0.2] # Pesos ajustados para sumar 1.0
            resultado = random.choices(resultados, weights=pesos, k=1)[0]

            logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Resultado: {resultado} ({tiempo_latencia:.1f}s)")

            # Modificación: Si requiere observación, transitar automáticamente a alta después de un tiempo simulado
            if resultado == "requiere_observacion":
                paciente.estado = 'observacion' # Estado intermedio
                logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Paciente requiere observación adicional.")
                logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Iniciando período de observación (2.8s)...")
                await asyncio.sleep(2.8) # Simular tiempo de observación
                paciente.estado = 'alta' # Transitar a alta
                logger.info(f"Paciente {paciente.id} [ALTA]: Observación completada, alta médica.")
            else:
                paciente.estado = 'alta' # Transitar a alta para otros resultados
                logger.info(f"Paciente {paciente.id} [ALTA]: Alta médica completada")

            await actualizar_estadisticas_func('alta')
            logger.info(f"Paciente {paciente.id} [SIMULACION]: Flujo completado con estado final '{paciente.estado}'.")


        except Exception as e:
            logger.error(f"Paciente {paciente.id} [ERROR SEGUIMIENTO]: Error en seguimiento: {type(e).__name__} - {e}", exc_info=True)
            paciente.estado = "error_seguimiento"
            await actualizar_estadisticas_func('error_seguimiento')
            logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo detenido debido a error en seguimiento.")

    # Assuming paciente object has an 'estado' attribute and actualizar_estadisticas_func is defined
    ```
    **Explicación:** Se modificó la lógica para que los pacientes en estado "requiere_observacion" transiten automáticamente a "alta" después de un tiempo simulado. Esto asegura que la tarea asíncrona de cada paciente finalice en el estado "alta" si llega a esta etapa sin errores graves.

## Relación con la Arquitectura

La implementación integra varios paradigmas y herramientas arquitectónicas:

* **AsyncIO:** Utilizado predominantemente en operaciones I/O bound (`asignar_cama_async`, `registrar_paciente_async`).
* **OOP (Programación Orientada a Objetos):** Evidente en la encapsulación lógica en la clase `Paciente` y la estructura de los modelos de ML (`diagnostico_ia.py`).
* **Funcional:** Se busca un enfoque funcional en módulos como `triage_ia.py` para minimizar efectos secundarios.
* **Concurrencia:** Manejada mediante semáforos para el control de recursos limitados y `ProcessPoolExecutor` para la paralelización de tareas CPU bound.

## Pruebas y Rendimiento

Se realizaron ejecuciones de la simulación para analizar el rendimiento bajo diferentes cargas de pacientes.

**Ejecución con 4 Pacientes:**

![image](https://github.com/user-attachments/assets/ee122bbd-c0f6-468a-aab9-8171882512d1)

**Salida Completa de la Simulación (Fragmento):**

03:29:44,873 🏥 [INFO] === SIMULACIÓN HOSPITALARIA INICIADA === 
03:29:44,874 🏥 [INFO] Pacientes a simular: 4 
03:29:44,874 🏥 [INFO] ==================================== 
03:29:44,875 🏥 [INFO] Paciente 1 [SIMULACION]: Paciente llega al hospital. 
03:29:45,983 📝 [INFO] Paciente 1 [REGISTRO]: Registrado en 1.11s | Avg: 1.11s 
03:29:48,227 🛏️ [INFO] Paciente 1 [CAMA]: Esperando cama disponible... 
03:29:52,039 💊 [INFO] Paciente 1 [TRATAMIENTO]: Tratamiento completado en 3.8s 
03:29:54,007 ✅ [INFO] Paciente 1 [ALTA]: Alta médica completada 
03:29:59,453 🏥 [INFO]
=== SIMULACIÓN COMPLETADA === 
============================================================ 
ESTADÍSTICAS FINALES DETALLADAS 
============================================================ 
│ Total registrados: 4 │ 
│ Procesados en triage: 4 │ 
│ Diagnosticados: 4 │ 
│ Pacientes que recibieron cama: 4 │ 
│ Pacientes con alta médica: 4 │ 
│ Altas sin cama asignada: 0 │ 
│ Errores durante registro: 0 │ 
│ Errores durante diagnóstico: 0 │ 
│ Errores durante cama: 0 │ 
│ Errores durante seguimiento: 0 │ 
│ Pacientes con errores/cancelados: 0 │ 
============================================================ 
03:29:59,456 🏥 [INFO] ⏱️ Tiempo total del proceso: 14.58 segundos    

**Análisis de Resultados:**

* Total Pacientes Simulados: 4 
* Pacientes que Iniciaron Flujo: 4
* Pacientes por Etapa:
    * Registrados: 4
    * Procesados en Triage: 4 
    * Diagnosticados: 4 
    * Recibieron Cama: 4 
* Estados Finales:
    * Alta Médica: 4 
    * Observación: 0 (Todos transitaron a alta tras observación si fue necesario)
    * Errores/Cancelados: 0 
* Tiempo Total de Simulación: 14.58 segundos 

**Análisis de Resultados (4 Pacientes):**

* Total Pacientes Simulados: 4
* Pacientes que Iniciaron Flujo: 4
* Pacientes por Etapa: Registrados (4), Procesados en Triage (4), Diagnosticados (4), Recibieron Cama (4).
* Estados Finales: Alta Médica (4), Observación (0), Errores/Cancelados (0).
* Tiempo Total de Simulación: 14.58 segundos.

**Interpretación:** La simulación con 4 pacientes valida la ejecución concurrente y la lógica modificada de alta tras observación. Los pacientes avanzan por las etapas concurrentemente gracias a `asyncio` y `ProcessPoolExecutor`. La modificación en seguimiento asegura que todos los pacientes, incluso si inicialmente requieren observación (Paciente 4), transiten a alta. El tiempo de simulación refleja el tiempo adicional simulado para la observación del Paciente 4. No se registraron errores, indicando un flujo exitoso.

**Resultados con Mayor Cantidad de Pacientes:**

* **Ejecución con 10 Pacientes:**

    ![image](https://github.com/user-attachments/assets/6e4ba4aa-ca59-4c07-a23c-ec4892e8ec12)

* **Ejecución con 30 Pacientes:**

    ![image](https://github.com/user-attachments/assets/35387214-59e5-495e-a976-80ae3afff9b9)

## Conclusión

La simulación demuestra eficazmente el uso de herramientas de concurrencia en Python (`asyncio`, `ProcessPoolExecutor`) para modelar un sistema complejo con diferentes tipos de tareas (I/O vs CPU bound) y recursos limitados. La integración de modelos de ML se realiza sin degradar el rendimiento del bucle principal. La modificación en la etapa de seguimiento introduce un proceso más realista donde los pacientes bajo observación eventualmente reciben el alta, validado por los resultados de las ejecuciones. La flexibilidad del modelo permite ajustar parámetros para analizar cuellos de botella y el impacto de los recursos en el flujo de pacientes under various scenarios.

## Referencias

* Durante el desarrollo de esta práctica, se utilizó una Inteligencia Artificial Gemini como herramienta auxiliar para diversos fines, de forma ética y documentada. La interacción se llevó a cabo principalmente entre el [Fecha de inicio de la conversación, ej. 01/05/2025].
* OpenAI. (2023). ChatGPT-4 [Modelo de lenguaje avanzado]. [https://chat.openai.com](https://chat.openai.com)
    * **Consultas relevantes (periodo de desarrollo 2025):**
        * Depuración de bloqueo en la asignación de camas (`asignacion_recursos.py`) relacionado con `asyncio.Semaphore`.
        * Sugerencia de diseño para un logger centralizado (`visualizacion.py`) utilizando el patrón Singleton.
