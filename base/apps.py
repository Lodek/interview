from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        try:
            self.create_bands()
        except Exception: #oof, gotta find a better way to solve this when there's no table
            pass

    def create_bands(self):
        from .models import Band
        bands = ['B1', 'B2', 'B3']
        for band in bands:
            Band.objects.get_or_create(band=band)
