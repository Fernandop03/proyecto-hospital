import asyncio
from concurrent.futures import ProcessPoolExecutor
from paciente import Paciente
from triage_ia import clasificar_prioridad
from diagnostico_ia import diagnosticar_paciente_sincrono
from asignacion_recursos import asignar_cama_async
from seguimiento import seguimiento_paciente
from registro import registrar_paciente_async
from visualizacion import mostrar_estadisticas, COLORES, COLOR_ETAPA, EMOJI_ETAPA, EtapaPaciente
import logging
import sys
from collections import defaultdict
import time
import random
import re

# --- Configuración de Logging Personalizada con Colores y Emojis ---

class ColoredFormatter(logging.Formatter):

    LOG_FORMAT = "%(message)s"

    def __init__(self, fmt=LOG_FORMAT):
        super().__init__(fmt)
        self.fmt = fmt
        self.time_fmt = "%H:%M:%S.%f"[:-3]

    def formatTime(self, record, datefmt=None):
        """Sobreescribe para formatear el tiempo y aplicarle color."""
        ct = self.converter(record.created)
        t = time.strftime(self.time_fmt, ct)
        s = "%s,%03d" % (t, record.msecs)
        return f"{COLORES['orange']}{s}{COLORES['reset']}"

    def format(self, record):
        """Sobreescribe para añadir color y emoji al mensaje."""
        original_message = super().format(record)

        # Intenta parsear el mensaje para encontrar la etapa (ej. Paciente X [ETAPA]: ...)
        match = re.match(r"Paciente (\d+) \[([A-Z_]+)\]: (.*)", original_message)

        etapa_key = 'simulacion'
        paciente_id = None
        mensaje_limpio = original_message

        if match:
            paciente_id = match.group(1)
            etapa_mayusculas = match.group(2)
            mensaje_limpio = match.group(3)
            etapa_key = etapa_mayusculas.lower()
            if etapa_key not in COLOR_ETAPA and etapa_mayusculas.lower() in map(str.lower, EtapaPaciente.__args__):
                 etapa_key = etapa_mayusculas.lower()
            elif etapa_mayusculas.lower() not in map(str.lower, EtapaPaciente.__args__):
                 if record.levelno >= logging.ERROR:
                     etapa_key = 'error'
                 else:
                     etapa_key = 'simulacion'

        color = COLOR_ETAPA.get(etapa_key, COLORES['reset'])
        emoji = EMOJI_ETAPA.get(etapa_key, '')

        level_name = record.levelname

        is_error_or_generic = (
            not match or
            record.levelno >= logging.ERROR or
            etapa_key in ['error', 'error_registro', 'error_diagnostico', 'error_cama', 'error_seguimiento', 'error_desconocido',
                          'flujo_cancelado', 'registro_cancelado', 'cama_cancelada', 'seguimiento_cancelado', 'error_triage',
                          'error_ejecutor_diagnostico', 'error_ejecutor_cama', 'error_ejecutor_seguimiento']
        )

        if is_error_or_generic:
             error_color = COLOR_ETAPA.get(etapa_key if etapa_key in COLOR_ETAPA else 'error', COLORES['red'])
             error_emoji = EMOJI_ETAPA.get(etapa_key if etapa_key in EMOJI_ETAPA else 'error', '❌')
             formatted_message = f"{error_emoji} [{level_name}] {error_color}{original_message}{COLORES['reset']}"
        else:
             paciente_part = f" Paciente {paciente_id}" if paciente_id else ""
             formatted_message = f"{emoji} [{level_name}] {color}{paciente_part} [{etapa_mayusculas}]{COLORES['reset']}: {mensaje_limpio}"

        return f"{self.formatTime(record)} {formatted_message}"


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

custom_formatter = ColoredFormatter()

if root_logger.handlers:
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(custom_formatter)

root_logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

# Configuración del sistema
PRIORIDAD_NUMERICA = {"Crítica": 0, "Alta": 1, "Media": 2, "Baja": 3}
# cola_triage ya no se usa

# Estadísticas globales (accedidas de forma asíncrona)
estadisticas_globales = defaultdict(int)
estadisticas_lock = asyncio.Lock()

async def actualizar_estadistica_global(etapa: str, cantidad: int = 1):
    """Actualiza las estadísticas globales de forma segura y asíncrona."""
    async with estadisticas_lock:
        estadisticas_globales[etapa] += cantidad
        logger.debug(f"Estadística '{etapa}' actualizada a {estadisticas_globales[etapa]}")

# --- Flujo Asíncrono por Paciente ---

async def flujo_paciente_async(paciente, cpu_executor: ProcessPoolExecutor):
    """
    Maneja el flujo completo de un paciente de forma asíncrona.
    Orquesta las diferentes etapas del proceso hospitalario.
    """
    logger.info(f"Paciente {paciente.id} [SIMULACION]: Iniciando flujo...")

    try:
        # 1. Registro (I/O bound)
        await registrar_paciente_async(paciente, actualizar_estadistica_global)
        if paciente.estado == "error_registro" or paciente.estado == "registro_cancelado":
             logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo detenido debido a {paciente.estado}.")
             return

        # 2. Triage (CPU rápido)
        logger.info(f"Paciente {paciente.id} [TRIAGE]: Iniciando triaje...")
        loop = asyncio.get_running_loop()
        try:
            paciente.prioridad = await loop.run_in_executor(
                cpu_executor, clasificar_prioridad, paciente.sintomas
            )
            logger.info(f"Paciente {paciente.id} [TRIAGE]: Prioridad {paciente.prioridad}")
            await actualizar_estadistica_global('triage')
        except Exception as e:
            logger.error(f"Paciente {paciente.id} [ERROR_TRIAGE]: Error en triaje: {type(e).__name__} - {e}", exc_info=True)
            paciente.estado = "error_triage"
            await actualizar_estadistica_global('error_triage')
            logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo detenido debido a error en triaje.")
            return

        # 3. Diagnóstico (CPU bound)
        logger.info(f"Paciente {paciente.id} [DIAGNOSTICO]: Iniciando diagnóstico...")
        try:
            paciente = await loop.run_in_executor(
                cpu_executor, diagnosticar_paciente_sincrono, paciente
            )
            if paciente.estado == "diagnosticado":
                await actualizar_estadistica_global('diagnostico')
            elif paciente.estado == "error_diagnostico":
                 logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo continuando sin diagnóstico debido a error.")

        except Exception as e:
            logger.error(f"Paciente {paciente.id} [ERROR_EJECUTOR_DIAGNOSTICO]: Error al ejecutar diagnóstico en executor: {type(e).__name__} - {e}", exc_info=True)
            paciente.estado = "error_ejecutor_diagnostico"
            await actualizar_estadistica_global('error_ejecutor_diagnostico')
            logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo continuando sin diagnóstico debido a error en executor.")

        # 4. Asignación de Cama y Tratamiento (Simulación de recurso limitado)
        recibio_cama = False
        if paciente.estado not in ["error_registro", "error_triage", "flujo_cancelado"]:
             try:
                recibio_cama = await asignar_cama_async(paciente, actualizar_estadistica_global)
             except Exception as e:
                 logger.error(f"Paciente {paciente.id} [ERROR_EJECUTOR_CAMA]: Error al ejecutar asignación de cama: {type(e).__name__} - {e}", exc_info=True)
                 paciente.estado = "error_ejecutor_cama"
                 await actualizar_estadistica_global('error_ejecutor_cama')
                 recibio_cama = False

        if paciente.estado in ["error_cama", "error_ejecutor_cama"]:
             logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo continuando sin cama debido a error.")

        # 5. Seguimiento (I/O bound)
        if paciente.estado not in ["alta", "error_registro", "error_triage", "flujo_cancelado", "cama_cancelada", "error_cama", "error_ejecutor_cama"]:
             logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Iniciando etapa de seguimiento...")
             try:
                 await seguimiento_paciente(paciente, actualizar_estadistica_global, recibio_cama)
             except Exception as e:
                 logger.error(f"Paciente {paciente.id} [ERROR_EJECUTOR_SEGUIMIENTO]: Error al ejecutar seguimiento: {type(e).__name__} - {e}", exc_info=True)
                 paciente.estado = "error_ejecutor_seguimiento"
                 await actualizar_estadistica_global('error_ejecutor_seguimiento')

        # 6. Finalización del Flujo del Paciente
        if paciente.estado not in ["error_registro", "error_triage", "error_diagnostico", "error_cama", "error_seguimiento",
                                   "flujo_cancelado", "registro_cancelado", "cama_cancelada", "seguimiento_cancelado",
                                   "error_ejecutor_diagnostico", "error_ejecutor_cama", "error_ejecutor_seguimiento"]:
             logger.info(f"Paciente {paciente.id} [SIMULACION]: Flujo completado con estado final '{paciente.estado}'.")

    except asyncio.CancelledError:
        logger.warning(f"Paciente {paciente.id} [SIMULACION]: Flujo cancelado.")
        paciente.estado = "flujo_cancelado"
        await actualizar_estadistica_global('flujo_cancelado')
    except Exception as e:
        logger.critical(f"Paciente {paciente.id} [ERROR_DESCONOCIDO]: Excepción no manejada en el flujo principal: {type(e).__name__} - {e}", exc_info=True)
        paciente.estado = "error_desconocido"
        await actualizar_estadistica_global('error_desconocido')



# --- Simulación de Llegadas (Asíncrona) ---

async def simular_llegadas_async(num_pacientes: int, cpu_executor: ProcessPoolExecutor):
    """
    Simula la llegada de pacientes y lanza una tarea asíncrona para cada uno.
    """
    tasks = []
    for i in range(num_pacientes):
        p = Paciente(i + 1)
        logger.info(f"Paciente {p.id} [SIMULACION]: Paciente llega al hospital.")
        task = asyncio.create_task(flujo_paciente_async(p, cpu_executor))
        tasks.append(task)
        await asyncio.sleep(random.uniform(0.1, 0.5))

    return tasks

# --- Función Principal de Ejecución ---

async def main(num_pacientes: int):
    """Función principal asíncrona para ejecutar la simulación."""
    tiempo_inicio = time.time()
    logger.info("=== SIMULACIÓN HOSPITALARIA INICIADA ===")
    logger.info(f"Pacientes a simular: {num_pacientes}")
    logger.info("====================================")

    with ProcessPoolExecutor() as cpu_executor:
        patient_flow_tasks = await simular_llegadas_async(num_pacientes, cpu_executor)
        results = await asyncio.gather(*patient_flow_tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"La tarea del paciente {i+1} terminó con una excepción no manejada en gather: {result}", exc_info=True)

    tiempo_total = time.time() - tiempo_inicio
    logger.info("\n=== SIMULACIÓN COMPLETADA ===")
    mostrar_estadisticas(estadisticas_globales)
    logger.info(f"⏱️ Tiempo total del proceso: {tiempo_total:.2f} segundos")

# --- Punto de Entrada del Script ---

if __name__ == "__main__":
    try:
        num_pacientes = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        asyncio.run(main(num_pacientes))
    except ValueError:
        logger.error("Por favor, proporcione un número válido de pacientes como argumento.")
    except KeyboardInterrupt:
        logger.info("\nSimulación interrumpida por el usuario.")
    except Exception as e:
        logger.critical(f"Error crítico no manejado durante la ejecución principal: {type(e).__name__} - {e}", exc_info=True)