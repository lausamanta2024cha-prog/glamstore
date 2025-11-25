#!/usr/bin/env python
"""
Script para simular presionar el botón "Enviar Correos Seleccionados" desde la web
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
from datetime import timedelta

def simular_boton_web():
    """Simula presionar el botón desde la web"""
    print("=== SIMULANDO PRESIONAR BOTÓN 'ENVIAR CORREOS SELECCIONADOS' ===")
    
    # Obtener repartidores con email
    repartidores_con_email = Repartidor.objects.filter(email__isnull=False).exclude(email='')
    
    if not repartidores_con_email.exists():
        print("❌ No hay repartidores con email")
        return
    
    # Seleccionar todos los repartidores con email (como si los hubiera seleccionado)
    repartidor_ids = [str(r.idRepartidor) for r in repartidores_con_email]
    
    print(f"Repartidores seleccionados: {repartidor_ids}")
    print()
    
    fecha = timezone.now().date()
    correos_enviados = 0
    errores = 0
    sin_email = 0
    sin_pedidos = 0
    
    print("🔄 Procesando repartidores...")
    print("-" * 50)
    
    for repartidor_id in repartidor_ids:
        try:
            repartidor = Repartidor.objects.get(idRepartidor=repartidor_id)
            print(f"\n📋 Procesando: {repartidor.nombreRepartidor} (ID: {repartidor_id})")
            
            # Verificar que tenga email
            if not repartidor.email:
                print(f"  ❌ Sin email")
                sin_email += 1
                continue
            
            print(f"  ✓ Email: {repartidor.email}")
            
            # Verificar que tenga pedidos (hoy o mañana)
            fecha_manana = fecha + timedelta(days=1)
            
            pedidos_hoy = Pedido.objects.filter(
                idRepartidor=repartidor,
                estado_pedido__in=['En Camino', 'Confirmado'],
                fechaCreacion__date=fecha
            ).count()
            
            pedidos_manana = Pedido.objects.filter(
                idRepartidor=repartidor,
                estado_pedido__in=['En Camino', 'Confirmado'],
                fechaCreacion__date=fecha_manana
            ).count()
            
            total_pedidos = pedidos_hoy + pedidos_manana
            print(f"  📦 Pedidos hoy: {pedidos_hoy}, Mañana: {pedidos_manana}, Total: {total_pedidos}")
            
            if total_pedidos == 0:
                print(f"  ❌ Sin pedidos")
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
                
        except Repartidor.DoesNotExist:
            print(f"  ❌ Repartidor no encontrado")
            errores += 1
            continue
        except Exception as e:
            print(f"  ❌ Excepción: {str(e)}")
            errores += 1
            continue
    
    # Mostrar resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE ENVÍO")
    print("=" * 50)
    print(f"✅ Correos enviados: {correos_enviados}")
    print(f"❌ Errores: {errores}")
    print(f"📧 Sin email: {sin_email}")
    print(f"📦 Sin pedidos: {sin_pedidos}")
    print(f"📊 Total seleccionados: {len(repartidor_ids)}")
    
    if correos_enviados > 0:
        print(f"\n🎉 {correos_enviados} correo(s) enviado(s) exitosamente")
    else:
        print(f"\n⚠️  No se enviaron correos")

def main():
    """Función principal"""
    print("INICIANDO SIMULACIÓN DE BOTÓN WEB")
    print("=" * 50)
    
    simular_boton_web()
    
    print("\nSIMULACIÓN COMPLETADA")

if __name__ == "__main__":
    main()