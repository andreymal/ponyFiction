from django.shortcuts import render


def handler403(request):
    return render(request, "error/403.html", dict(page_title="403 — доступ запрещён"), status=403)


def handler404(request):
    return render(request, "error/404.html", dict(page_title="404 — книга не найдена"), status=404)


def handler500(request):
    return render(request, "error/500.html", dict(page_title="500 — внутренняя ошибка сервера"), status=500)
