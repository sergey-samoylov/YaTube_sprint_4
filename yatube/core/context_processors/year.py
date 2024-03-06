import datetime


def year(request):
    """Добавляет переменную с текущим годом во все файлы проекта."""
    return {
        # datetime.now()
        'year': datetime.datetime.now().year
    }
