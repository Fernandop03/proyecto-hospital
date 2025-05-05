# visualizacion.py
# Este archivo contendrá las definiciones de colores y emojis,
# y la función para mostrar estadísticas finales.
import logging
import sys
from typing import Literal

# Definición de tipos para etapas
# Mantener esta lista actualizada con las etapas usadas en los logs
EtapaPaciente = Literal[
    'registro',
    'triage',
    'diagnostico',
    'cama',
    'tratamiento',
    'seguimiento',
    'alta',
    'error',
    'estado',
    'simulacion', # Para eventos generales de simulación
    'estadisticas', # Para logs relacionados con estadísticas
    'flujo_cancelado', # Estados de error/cancelación
    'registro_cancelado',
    'cama_cancelada',
    'seguimiento_cancelado',
    'error_registro',
    'error_diagnostico',
    'error_cama',
    'error_seguimiento',
    'error_desconocido',
    'error_triage', # Nuevo estado de error en triaje
    'error_ejecutor_diagnostico', # Errores al ejecutar en executor
    'error_ejecutor_cama',
    'error_ejecutor_seguimiento'
]

# Códigos de colores ANSI
# Usaremos estos para colorear las diferentes partes del log
COLORES = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'blue': '\033[94m',    # Registro, Simulación (general)
    'yellow': '\033[93m',  # Triage
    'cyan': '\033[96m',    # Diagnóstico
    'green': '\033[92m',   # Cama, Tratamiento
    'magenta': '\033[95m', # Seguimiento
    'red': '\033[91m',     # Alta, Errores (general, estado de error)
    'grey': '\033[90m',    # Estado (cambios), Estadísticas (log de actualización)
    'orange': '\033[38;5;208m', # Un color diferente para el timestamp
}

# Mapeo de etapas a colores
COLOR_ETAPA = {
    'registro': COLORES['blue'],
    'triage': COLORES['yellow'],
    'diagnostico': COLORES['cyan'],
    'cama': COLORES['green'],
    'tratamiento': COLORES['green'],
    'seguimiento': COLORES['magenta'],
    'alta': COLORES['red'],
    'error': COLORES['red'], # Fallback para logs de error genéricos
    'estado': COLORES['grey'],
    'simulacion': COLORES['blue'],
    'estadisticas': COLORES['grey'],
    'flujo_cancelado': COLORES['red'],
    'registro_cancelado': COLORES['red'],
    'cama_cancelada': COLORES['red'],
    'seguimiento_cancelado': COLORES['red'],
    'error_registro': COLORES['red'],
    'error_diagnostico': COLORES['red'],
    'error_cama': COLORES['red'],
    'error_seguimiento': COLORES['red'],
    'error_desconocido': COLORES['red'],
    'error_triage': COLORES['red'],
    'error_ejecutor_diagnostico': COLORES['red'],
    'error_ejecutor_cama': COLORES['red'],
    'error_ejecutor_seguimiento': COLORES['red'],
}

# Mapeo de etapas a emojis
EMOJI_ETAPA = {
    'registro': '📝',  # Notas
    'triage': '⚠️',    # Advertencia/Prioridad
    'diagnostico': '🩺', # Estetoscopio
    'cama': '🛏️',      # Cama de hospital
    'tratamiento': '💊', # Píldora/Medicina
    'seguimiento': '👁️‍🗨️', # Ojo en bocadillo (observación/seguimiento)
    'alta': '✅',      # Marca de verificación (alta exitosa)
    'error': '❌',     # Cruz roja (error)
    'estado': '🔄',    # Símbolo de reciclaje (cambio de estado)
    'simulacion': '🏥', # Hospital (eventos generales de simulación)
    'estadisticas': '📊', # Gráfico de barras
    'flujo_cancelado': '🛑', # Señal de stop (flujo detenido)
    'registro_cancelado': '🛑',
    'cama_cancelada': '🛑',
    'seguimiento_cancelado': '🛑',
    'error_registro': '❗', # Signo de exclamación (error específico)
    'error_diagnostico': '❗',
    'error_cama': '❗',
    'error_seguimiento': '❗',
    'error_desconocido': '❓', # Signo de interrogación (error desconocido)
    'error_triage': '❗',
    'error_ejecutor_diagnostico': '❗',
    'error_ejecutor_cama': '❗',
    'error_ejecutor_seguimiento': '❗',
}


# Mantener la función de estadísticas, ya que es de presentación al final
def mostrar_estadisticas(estadisticas):
    print("\n" + "="*60)
    print("ESTADÍSTICAS FINALES DETALLADAS".center(60))
    print("="*60)
    # Usar .get(key, 0) para manejar casos donde una etapa no ocurrió
    print(f"│ {'Total registrados:':<30} {estadisticas.get('registro', 0):>25} │")
    print(f"│ {'Procesados en triage:':<30} {estadisticas.get('triage', 0):>25} │")
    print(f"│ {'Diagnosticados:':<30} {estadisticas.get('diagnostico', 0):>25} │")
    print(f"│ {'Pacientes que recibieron cama:':<30} {estadisticas.get('cama_asignada', 0):>25} │")
    print(f"│ {'Pacientes con alta médica:':<30} {estadisticas.get('alta', 0):>25} │")
    print(f"│ {'Altas sin cama asignada:':<30} {estadisticas.get('alta_sin_cama', 0):>25} │")
    print(f"│ {'Errores durante registro:':<30} {estadisticas.get('error_registro', 0):>25} │")
    print(f"│ {'Errores durante diagnóstico:':<30} {estadisticas.get('error_diagnostico', 0):>25} │")
    print(f"│ {'Errores durante cama:':<30} {estadisticas.get('error_cama', 0):>25} │")
    print(f"│ {'Errores durante seguimiento:':<30} {estadisticas.get('error_seguimiento', 0):>25} │")
    total_errores_cancelaciones = sum(v for k, v in estadisticas.items() if k.startswith(('error_', 'flujo_cancelado', 'registro_cancelado', 'cama_cancelada', 'seguimiento_cancelado')))
    print(f"│ {'Pacientes con errores/cancelados:':<30} {total_errores_cancelaciones:>25} │")
    print("="*60)