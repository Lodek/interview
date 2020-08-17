from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        try:
            self.create_seniority()
        except Exception: #oof, gotta find a better way to solve this when there's no table
            pass

    def create_seniority(self):
        from .models import Seniority
        seniorities = ['JR', 'PL', 'SR', 'LD']
        for seniority in seniorities:
            Seniority.objects.get_or_create(seniority=seniority)
