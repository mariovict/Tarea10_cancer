"""Entrena la Regresión Logística (Tarea 8) y guarda el modelo para Django.

Uso:  python train_model.py
"""
import joblib

from predictor.ml import RUTA_MODELO, entrenar_modelo, texto_ejemplo

modelo, exactitud = entrenar_modelo()
joblib.dump(modelo, RUTA_MODELO)
print(f"Modelo guardado en {RUTA_MODELO}")
print(f"Exactitud en el conjunto de prueba: {exactitud:.4f}")

with open("ejemplo_casos.csv", "w", encoding="utf-8") as f:
    f.write(texto_ejemplo() + "\n")
print("Archivo de ejemplo escrito: ejemplo_casos.csv")
