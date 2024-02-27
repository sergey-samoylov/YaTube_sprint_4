from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
    )

"""
в каждом объекте модели User автоматически будет создано свойство с таким же названием (posts), и в нём будут храниться ссылки на все объекты модели Post, которые ссылаются на объект User.
На практике это означает, что в объекте записи есть поле author, в котором хранится ссылка на автора (например, на пользователя admin), а в объекте пользователя admin появилось поле posts, в котором хранятся ссылки на все посты этого автора. И теперь можно получить список постов автора, обратившись к его свойству posts.
"""
