from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'

    def ready(self, news=None):
        pass
       # from News import signals #не импортируется
