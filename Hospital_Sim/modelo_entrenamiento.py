import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import random

def generar_datos(n=1000):
    """Genera datos sintéticos de pacientes"""
    sintomas = []
    enfermedades = []
    prioridades = []

    for _ in range(n):
        fiebre = random.randint(0, 1)
        tos = random.randint(0, 1)
        dolor = random.randint(0, 1)
        fatiga = random.randint(0, 1)
        respirar = random.randint(0, 1)

        # Reglas simples para prioridad y diagnóstico
        if respirar and fiebre:
            enfermedad = "COVID-19"
            prioridad = "Crítica"
        elif fiebre and tos:
            enfermedad = "Gripe"
            prioridad = "Alta"
        elif dolor and fatiga:
            enfermedad = "Infección"
            prioridad = "Media"
        else:
            enfermedad = "Común"
            prioridad = "Baja"

        sintomas.append([fiebre, tos, dolor, fatiga, respirar])
        enfermedades.append(enfermedad)
        prioridades.append(prioridad)

    return pd.DataFrame(
        sintomas, 
        columns=["fiebre", "tos", "dolor", "fatiga", "respirar"]
    ).assign(
        enfermedad=enfermedades,
        prioridad=prioridades
    )

def entrenar_modelos():
    """Entrena y guarda los modelos de clasificación"""
    df = generar_datos()
    
    # Codificación de etiquetas
    le_enf = LabelEncoder()
    le_prio = LabelEncoder()
    
    df["enfermedad_cod"] = le_enf.fit_transform(df["enfermedad"])
    df["prioridad_cod"] = le_prio.fit_transform(df["prioridad"])
    
    # Datos para entrenamiento
    X = df[["fiebre", "tos", "dolor", "fatiga", "respirar"]]
    y_diag = df["enfermedad_cod"]
    y_prio = df["prioridad_cod"]
    
    # Modelo de diagnóstico
    X_train, X_test, y_train, y_test = train_test_split(X, y_diag, test_size=0.2)
    clf_diag = DecisionTreeClassifier(max_depth=5)
    clf_diag.fit(X_train, y_train)
    
    # Modelo de triage
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y_prio, test_size=0.2)
    clf_triage = DecisionTreeClassifier(max_depth=4)
    clf_triage.fit(X_train2, y_train2)
    
    # Guardar modelos
    joblib.dump(clf_diag, "modelo_diagnostico.pkl")
    joblib.dump(clf_triage, "modelo_triage.pkl")
    joblib.dump(le_enf, "label_enfermedad.pkl")
    joblib.dump(le_prio, "label_prioridad.pkl")
    
    print("✅ Modelos entrenados y guardados")

if __name__ == "__main__":
    entrenar_modelos()
