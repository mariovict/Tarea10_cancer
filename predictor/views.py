from .ml import N_FEATURES, NOMBRES_FEATURES, parsear_casos, predecir, texto_ejemplo
from django.shortcuts import render


def index(request):
    contexto = {"n_features": N_FEATURES, "nombres": NOMBRES_FEATURES,
                "texto": "", "resultados": None, "error": None}

    if request.method == "POST":
        texto = request.POST.get("casos", "")
        archivo = request.FILES.get("archivo")
        if archivo:
            texto = archivo.read().decode("utf-8-sig", errors="replace")
        contexto["texto"] = texto
        try:
            X = parsear_casos(texto)
            contexto["resultados"] = predecir(X)
        except ValueError as e:
            contexto["error"] = str(e)
    elif request.GET.get("ejemplo"):
        contexto["texto"] = texto_ejemplo()

    return render(request, "predictor/index.html", contexto)
