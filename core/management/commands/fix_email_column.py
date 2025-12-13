from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Aumenta el tamaño del campo email en la tabla usuarios'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Verificar el tamaño actual
                cursor.execute("""
                    SELECT character_maximum_length
                    FROM information_schema.columns
                    WHERE table_name = 'usuarios' AND column_name = 'email';
                """)
                result = cursor.fetchone()
                current_size = result[0] if result else None
                
                if current_size == 255:
                    self.stdout.write(self.style.SUCCESS('✓ Campo email ya tiene 255 caracteres'))
                    return
                
                self.stdout.write(f'Aumentando tamaño del campo email de {current_size} a 255...')
                
                cursor.execute("""
                    ALTER TABLE usuarios
                    ALTER COLUMN email TYPE character varying(255);
                """)
            
            self.stdout.write(self.style.SUCCESS('✓ Campo email actualizado a 255 caracteres'))
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Error: {str(e)}'))
