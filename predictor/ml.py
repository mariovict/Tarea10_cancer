"""Modelo predictivo (Regresión Logística) para cáncer de mama.

Dataset: Breast Cancer Wisconsin (Diagnostic) incluido en scikit-learn.
En ese dataset: clase 0 = maligno, clase 1 = benigno.
"""
import re
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

RUTA_MODELO = Path(__file__).resolve().parent / "modelo_cancer.joblib"
MAX_CASOS = 500

_datos = load_breast_cancer()
NOMBRES_FEATURES = list(_datos.feature_names)
N_FEATURES = len(NOMBRES_FEATURES)  # 30
ETIQUETAS = {0: "Maligno", 1: "Benigno"}


def entrenar_modelo():
    """Entrena el pipeline (escalado + regresión logística).

    Devuelve (modelo, exactitud_en_prueba).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        _datos.data, _datos.target, test_size=0.2, random_state=42,
        stratify=_datos.target,
    )
    modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    modelo.fit(X_train, y_train)
    return modelo, modelo.score(X_test, y_test)


@lru_cache(maxsize=1)
def cargar_modelo():
    """Carga el modelo guardado; si falta o es incompatible, lo reentrena."""
    try:
        return joblib.load(RUTA_MODELO)
    except Exception:
        modelo, _ = entrenar_modelo()
        return modelo


def parsear_casos(texto):
    """Convierte texto (una fila por caso, 30 valores separados por coma,
    punto y coma o tabulador) en una matriz numpy de shape (n_casos, 30).

    Una primera línea con encabezados se ignora. Lanza ValueError con un
    mensaje claro si algo no cuadra.
    """
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    filas = []
    for i, linea in enumerate(lineas, start=1):
        partes = [p for p in re.split(r"[,;\t]+", linea) if p.strip()]
        try:
            valores = [float(p) for p in partes]
        except ValueError:
            if i == 1:  # encabezado
                continue
            raise ValueError(f"La línea {i} contiene valores que no son números.")
        if len(valores) != N_FEATURES:
            raise ValueError(
                f"La línea {i} tiene {len(valores)} valores; "
                f"cada caso necesita exactamente {N_FEATURES}."
            )
        filas.append(valores)
    if not filas:
        raise ValueError("No se ingresó ningún caso.")
    if len(filas) > MAX_CASOS:
        raise ValueError(f"Máximo {MAX_CASOS} casos por envío.")
    return np.array(filas, dtype=float)


def predecir(X):
    """Devuelve una lista de dicts con la predicción y predict_proba por caso."""
    modelo = cargar_modelo()
    probas = modelo.predict_proba(X)
    clases = list(modelo.classes_)
    resultados = []
    for i, fila in enumerate(probas, start=1):
        p = {int(c): float(fila[j]) for j, c in enumerate(clases)}
        clase = max(p, key=p.get)
        resultados.append({
            "caso": i,
            "diagnostico": ETIQUETAS[clase],
            "es_maligno": clase == 0,
            "prob_maligno": round(p[0] * 100, 2),
            "prob_benigno": round(p[1] * 100, 2),
            "confianza": round(p[clase] * 100, 2),
        })
    return resultados


def texto_ejemplo():
    """Encabezado + un caso maligno y uno benigno reales del dataset."""
    i_mal = int(np.where(_datos.target == 0)[0][0])
    i_ben = int(np.where(_datos.target == 1)[0][0])
    lineas = [",".join(NOMBRES_FEATURES)]
    for i in (i_mal, i_ben):
        lineas.append(",".join(repr(float(v)) for v in _datos.data[i]))
    return "\n".join(lineas)
