from django.core.management.base import BaseCommand
from core.models.configuracion import ConfiguracionGlobal


class Command(BaseCommand):
    help = 'Inicializa la configuración global con el margen de ganancia'

    def handle(self, *args, **options):
        config, created = ConfiguracionGlobal.objects.get_or_create(pk=1)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Configuración global creada con margen: {config.margen_ganancia}%'))
        else:
            self.stdout.write(self.style.WARNING(f'Configuración global ya existe con margen: {config.margen_ganancia}%'))
