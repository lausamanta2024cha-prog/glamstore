#!/usr/bin/env python
"""
Script para probar el envío de correos a repartidores seleccionados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.utils import timezone
from core.models.repartidores import Repartidor
from core.models.pedidos import Pedido
from core.Gestion_admin.services_repartidores import enviar_correo_repartidor_detallado

def test_envio_masivo():
    """Prueba el envío masivo de correos"""
    print("=== PROBANDO ENVÍO MASIVO DE CORREOS ===")
    
    # Obtener repartidores con email
    repartidores_con_email = Repartidor.objects.filter(email__isnull=False).exclude(email='')
    
    if not repartidores_con_email.exists():
        print("No hay repartidores con email configurado")
        return
    
    fecha = timezone.now().date()
    correos_enviados = 0
    errores = 0
    sin_email = 0
    sin_pedidos = 0
    
    print(f"Fecha de procesamiento: {fecha}")
    print(f"Repartidores a procesar: {repartidores_con_email.count()}")
    print()
    
    for repartidor in repartidores_con_email:
        print(f"Procesando: {repartidor.nombreRepartidor} ({repartidor.email})")
        
        try:
            # Verificar que tenga email
            if not repartidor.email:
                print(f"  ❌ Sin email")
                sin_email += 1
                continue
            
            # Verificar que tenga pedidos
            pedidos = Pedido.objects.filter(
                idRepartidor=repartidor,
                estado_pedido__in=['En Camino', 'Confirmado'],
                fechaCreacion__date=fecha
            ).count()
            
            print(f"  📦 Pedidos encontrados: {pedidos}")
            
            if pedidos == 0:
                print(f"  ❌ Sin pedidos para hoy")
                sin_pedidos += 1
                continue
            
            # Intentar enviar correo detallado
            print(f"  📧 Enviando correo...")
            if enviar_correo_repartidor_detallado(repartidor, fecha):
                print(f"  ✅ Correo enviado exitosamente")
                correos_enviados += 1
            else:
                print(f"  ❌ Error al enviar correo")
                errores += 1
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            errores += 1
            continue
        
        print()
    
    # Mostrar resumen
    print("=" * 50)
    print("RESUMEN DE ENVÍO")
    print("=" * 50)
    print(f"✅ Correos enviados exitosamente: {correos_enviados}")
    print(f"❌ Errores en envío: {errores}")
    print(f"📧 Repartidores sin email: {sin_email}")
    print(f"📦 Repartidores sin pedidos: {sin_pedidos}")
    print(f"📊 Total procesados: {repartidores_con_email.count()}")

def main():
    """Función principal"""
    print("INICIANDO PRUEBA DE ENVÍO MASIVO")
    print("=" * 50)
    
    test_envio_masivo()
    
    print("\nPRUEBA COMPLETADA")

if __name__ == "__main__":
    main()