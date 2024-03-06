# core/templatetags/user_filters.py
from random import choice
from django import template

from os.path import join as path_join
from os import listdir
from os.path import isfile

# В template.Library зарегистрированы все встроенные теги и фильтры шаблонов;
# добавляем к ним и наш фильтр.
register = template.Library()


@register.filter
def addclass(field, css):
    """Фильтр указывает CSS-класс в HTML любого поля формы."""
    return field.as_widget(attrs={'class': css})

# синтаксис @register... , под который описана функция addclass() - 
# это применение "декораторов", функций, меняющих поведение функций

@register.simple_tag
def random_img():
    """Вставка случайной картинки в публикацию."""
    dir_path = 'static/img/random'
    files = [
        content for content in listdir(dir_path) if isfile(
            path_join(dir_path, content),
        )
    ]
    return f'static/img/random/{choice(files)}'
