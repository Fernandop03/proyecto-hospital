import asyncio
import random
import logging # Importar logging

# Configurar un logger
logger = logging.getLogger(__name__)

# Asumimos que la función actualizar_estadisticas_func se pasa como argumento.

async def seguimiento_paciente(paciente, actualizar_estadisticas_func, recibio_cama=False):
    if paciente.estado in ['alta', 'error_registro', 'error_diagnostico', 'error_cama', 'seguimiento_cancelado']:
        return

    logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Iniciando seguimiento...")

    try:
        # Simular latencia de red
        tiempo_latencia = random.uniform(1, 3)
        await asyncio.sleep(tiempo_latencia)

        resultados = ["estable", "mejorando", "requiere_observacion"]
        pesos = [0.4, 0.4, 0.2] 
        resultado = random.choices(resultados, weights=pesos, k=1)[0]

        logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Resultado: {resultado} ({tiempo_latencia:.1f}s)")

        # Actualizar estado y registrar alta si corresponde
        if resultado != "requiere_observacion":
            paciente.estado = "alta"
            logger.info(f"Paciente {paciente.id} [ALTA]: Alta médica completada")
            await actualizar_estadisticas_func('alta')
            if not recibio_cama:
                await actualizar_estadisticas_func('alta_sin_cama')
        else:
            # --- INICIO DE MODIFICACIÓN SUGERIDA ---
            paciente.estado = "observacion"
            logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Paciente requiere observación adicional.")
            await actualizar_estadisticas_func('observacion') # Opcional: registrar cuántos pasan a observación

            # Simular período de observación adicional
            tiempo_observacion = random.uniform(1, 3) # Tiempo adicional en observación
            logger.info(f"Paciente {paciente.id} [SEGUIMIENTO]: Iniciando período de observación ({tiempo_observacion:.1f}s)...")
            await asyncio.sleep(tiempo_observacion)

            # Después del período de observación, el paciente recibe el alta
            paciente.estado = "alta"
            logger.info(f"Paciente {paciente.id} [ALTA]: Observación completada, alta médica.")
            await actualizar_estadisticas_func('alta')
            # Si el paciente no recibió cama inicialmente pero pasó por observación,
            # puedes decidir si contarlo como alta sin cama o no.
            # Si quieres contarlo como alta sin cama si NO recibió cama, mantén esta línea:
            if not recibio_cama:
                 await actualizar_estadisticas_func('alta_sin_cama')
            # --- FIN DE MODIFICACIÓN SUGERIDA ---


    except asyncio.CancelledError:
        logger.warning(f"Paciente {paciente.id} [SEGUIMIENTO]: Tarea de seguimiento cancelada.")
        paciente.estado = "seguimiento_cancelado"
        # No actualizar estadística de error si fue cancelado
    except Exception as e:
        # Loguear el error específico y actualizar estado/estadística de error
        error_msg = f"Error en seguimiento: {type(e).__name__} - {str(e)}"
        logger.error(f"Paciente {paciente.id} [ERROR]: {error_msg}", exc_info=True)
        paciente.estado = "error_seguimiento"
        await actualizar_estadisticas_func('error_seguimiento')