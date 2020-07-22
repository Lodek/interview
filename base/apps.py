from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        self.create_bands()

    def create_bands(self):
        from .models import Band
        bands = ['B1', 'B2', 'B3']
        for band in bands:
            Band.objects.get_or_create(band=band)
