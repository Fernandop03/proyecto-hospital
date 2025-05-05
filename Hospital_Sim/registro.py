
import time
import random
import logging # Importar logging
import asyncio # Importar asyncio

# Configurar un logger
logger = logging.getLogger(__name__)

# Estadísticas de registro (tiempos). Accedido solo desde el contexto asíncrono principal ahora.
tiempos_registro = []
registro_lock = asyncio.Lock() # Cambiar a asyncio.Lock

async def registrar_paciente_async(paciente, actualizar_estadisticas_func):
    """
    Simula el registro de un paciente con latencia aleatoria de forma asíncrona.
    Operación I/O bound - adecuada para asyncio.

    Args:
        paciente: Objeto Paciente a registrar
        actualizar_estadisticas_func: Función asíncrona para actualizar estadísticas globales.
    """
    inicio = time.time() # time.time() es síncrono, lo cual está bien aquí

    try:
        # Simular latencia de red/DB
        latencia = random.uniform(0.5, 2.0)
        await asyncio.sleep(latencia) # Usar await asyncio.sleep

        # Registrar tiempo (protegido por lock asíncrono)
        duracion = time.time() - inicio
        async with registro_lock: # Usar async with para asyncio.Lock
            tiempos_registro.append(duracion)
            # El cálculo del promedio no modifica la lista, puede llamarse sin lock *si no se modifica la lista*
            # Pero aquí es seguro dentro del lock.
            avg_actual = promedio_registro_sincrono()

        # Log exitoso
        logger.info(f"Paciente {paciente.id} [REGISTRO]: Registrado en {duracion:.2f}s | Avg: {avg_actual:.2f}s")

        paciente.estado = "registrado"
        await actualizar_estadisticas_func('registro') # Actualizar estadística centralizadamente

    except asyncio.CancelledError:
         logger.warning(f"Paciente {paciente.id} [REGISTRO]: Tarea de registro cancelada.")
         paciente.estado = "registro_cancelado"
         # No actualizar estadística de error si fue cancelado
    except Exception as e:
        # Loguear el error específico y actualizar estado/estadística de error
        error_msg = f"Error en registro: {type(e).__name__} - {str(e)}"
        logger.error(f"Paciente {paciente.id} [ERROR]: {error_msg}", exc_info=True) # exc_info=True para loguear traceback
        paciente.estado = "error_registro"
        await actualizar_estadisticas_func('error_registro')


def promedio_registro_sincrono():
    """Calcula el tiempo promedio de registro (debe llamarse con el lock adquirido o en un contexto seguro)"""
    # Esta función es síncrona y accede a tiempos_registro.
    # Si se llama fuera del lock, debe ser llamada con el lock adquirido.
    # Asumiremos que las llamadas relevantes se hacen de forma segura.
    if not tiempos_registro:
        return 0
    return sum(tiempos_registro) / len(tiempos_registro)


def estadisticas_registro():
    if not tiempos_registro:
        return {'total': 0, 'promedio': 0, 'max': 0, 'min': 0}
    return {
        'total': len(tiempos_registro),
        'promedio': promedio_registro_sincrono(), # Usar la función auxiliar
        'max': max(tiempos_registro),
        'min': min(tiempos_registro)
    }