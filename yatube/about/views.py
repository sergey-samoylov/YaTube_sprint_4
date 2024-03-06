from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Автор - Сергей Самойлов"

        context = {
            'title': title,
        }

        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Технологии данного проекта"
        tech_used = (
            "Vim 9.1.80",
            "Python 3.11",
            "Django 5.0.2",
        )

        context = {
            'title': title,
            'tech_used': tech_used,
        }

        return context
