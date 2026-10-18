# Tarea 10 – Predicción de cáncer de seno (Django + Heroku)

## Probar en local
    python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python train_model.py          # regenera modelo_cancer.joblib (opcional)
    DEBUG=True python manage.py runserver   # Windows (cmd): set DEBUG=True && python manage.py runserver
Abre http://127.0.0.1:8000 y usa "Cargar dos casos de ejemplo".

## Desplegar en Heroku
    git init && git add . && git commit -m "Tarea 10"
    heroku login
    heroku create nombre-unico-app
    heroku config:set SECRET_KEY="una-clave-larga-y-aleatoria"
    heroku config:set CSRF_TRUSTED_ORIGINS="https://nombre-unico-app.herokuapp.com"
    git push heroku main          # (o master, según tu rama)
    heroku open

Si el push falla por la versión de Python, crea `runtime.txt` con `python-3.12.x`
(según lo que indique Heroku) en lugar de `.python-version`.
