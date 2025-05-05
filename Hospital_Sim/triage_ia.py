
import joblib
from sklearn.tree import DecisionTreeClassifier
import logging # Importar logging

# Configurar un logger
logger = logging.getLogger(__name__)

# Cargar modelo pre-entrenado
try:
    modelo_triage = joblib.load("modelo_triage.pkl")
    label_prioridad = joblib.load("label_prioridad.pkl")
    logger.info("Modelos de triage cargados exitosamente.")
except FileNotFoundError:
    logger.critical("Modelos de triage no encontrados. Ejecute modelo_entrenamiento.py primero.", exc_info=True)
    raise ImportError("Modelos de triage no encontrados. Ejecute modelo_entrenamiento.py primero")
except Exception as e:
    logger.critical(f"Error al cargar modelos de triage: {type(e).__name__} - {str(e)}", exc_info=True)
    raise # Re-lanzar la excepción


def clasificar_prioridad(sintomas_dict):
    sintomas = [
        sintomas_dict.get("fiebre", 0),
        sintomas_dict.get("tos", 0),
        sintomas_dict.get("dolor", 0),
        sintomas_dict.get("fatiga", 0),
        sintomas_dict.get("respirar", 0),
    ]

    # No loguear el triaje aquí, se hará en main.py después de obtener el resultado.
    pred = modelo_triage.predict([sintomas])[0]
    return label_prioridad.inverse_transform([pred])[0]