import random

class Paciente:
    def __init__(self, id, sintomas=None):
        """
        Representa un paciente en el sistema hospitalario.

        Args:
            id: Identificador único del paciente
            sintomas: Diccionario de síntomas (opcional, se generan aleatorios si no se proporciona)
        """
        self.id = id
        self.sintomas = sintomas if sintomas else self.generar_sintomas()
        self.prioridad = None
        self.diagnostico = None
        self.estado = "registrado" # Estado inicial

    def generar_sintomas(self):
        """Genera síntomas aleatorios para simulación"""
        # Asegurarse de que los síntomas estén en el orden esperado por los modelos ML
        return {
            "fiebre": random.randint(0, 1),
            "tos": random.randint(0, 1),
            "dolor": random.randint(0, 1),
            "fatiga": random.randint(0, 1),
            "respirar": random.randint(0, 1)
        }

    def __str__(self):
        return (f"Paciente {self.id} | Prioridad: {self.prioridad} | "
                f"Diagnóstico: {self.diagnostico} | Estado: {self.estado}")