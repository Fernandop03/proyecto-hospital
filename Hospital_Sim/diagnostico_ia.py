import joblib
import pandas as pd
import logging # Importar logging

# Configurar un logger
logger = logging.getLogger(__name__)

# Cargar modelo pre-entrenado
try:
    modelo_diagnostico = joblib.load("modelo_diagnostico.pkl")
    label_enfermedad = joblib.load("label_enfermedad.pkl")
    logger.info("Modelos de diagnóstico cargados exitosamente.")
except FileNotFoundError:
     logger.critical("Modelos de diagnóstico no encontrados. Ejecute modelo_entrenamiento.py primero.", exc_info=True)
     raise ImportError("Modelos de diagnóstico no encontrados. Ejecute modelo_entrenamiento.py primero")
except Exception as e:
    logger.critical(f"Error al cargar modelos de diagnóstico: {type(e).__name__} - {str(e)}", exc_info=True)
    raise # Re-lanzar la excepción


def diagnosticar_sincrono(sintomas):
    df = pd.DataFrame([sintomas])
    codigo = modelo_diagnostico.predict(df)[0]
    return label_enfermedad.inverse_transform([codigo])[0]


def diagnosticar_paciente_sincrono(paciente):
    """
    Realiza diagnóstico para un solo paciente y actualiza su estado.
    Diseñado para ejecutarse en un executor (síncrono).

    Args:
        paciente: Objeto Paciente
    Returns:
        Objeto Paciente con diagnóstico actualizado
    """
    try:
        paciente.diagnostico = diagnosticar_sincrono(paciente.sintomas)
        paciente.estado = "diagnosticado"
        # El log se hará en main.py después de obtener el resultado
        # logger.info(f"Paciente {paciente.id} [DIAGNOSTICO]: {paciente.diagnostico}")
        return paciente
    except Exception as e:
         logger.error(f"Paciente {paciente.id} [ERROR]: Error en diagnóstico: {type(e).__name__} - {e}", exc_info=True)
         paciente.estado = "error_diagnostico"
         return paciente # Retornar paciente incluso con error

# Eliminar la función diagnostico_batch si ya no se utiliza en main.py
# def diagnostico_batch(paciente): ...