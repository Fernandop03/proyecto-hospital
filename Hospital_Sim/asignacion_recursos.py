import asyncio 
import random
import logging 


logger = logging.getLogger(__name__)

camas_disponibles = asyncio.Semaphore(3) 

async def asignar_cama_async(paciente, actualizar_estadisticas_func):
    logger.info(f"Paciente {paciente.id} [CAMA]: Esperando cama disponible...")

    try:
        # Intentar adquirir el semáforo asíncrono
        async with camas_disponibles:
            logger.info(f"Paciente {paciente.id} [CAMA]: Cama asignada - Iniciando tratamiento")

            # Registrar cama asignada
            await actualizar_estadisticas_func('cama_asignada')

            # Simular tiempo de tratamiento
            tiempo_tratamiento = random.uniform(2, 5)
            await asyncio.sleep(tiempo_tratamiento) # Usar await asyncio.sleep

            logger.info(f"Paciente {paciente.id} [TRATAMIENTO]: Tratamiento completado en {tiempo_tratamiento:.1f}s")
            paciente.estado = "tratamiento_completado" # Nuevo estado para indicar fin del tratamiento
            return True  # Indica que sí recibió cama

    except asyncio.CancelledError:
        logger.warning(f"Paciente {paciente.id} [CAMA]: Tarea de asignación/tratamiento cancelada.")
        paciente.estado = "cama_cancelada"
        return False # No recibió cama si fue cancelado
    except Exception as e:
         logger.error(f"Paciente {paciente.id} [ERROR]: Error en asignación/tratamiento: {type(e).__name__} - {e}", exc_info=True)
         paciente.estado = "error_cama"
         await actualizar_estadisticas_func('error_cama')
         return False # No recibió cama si hubo error