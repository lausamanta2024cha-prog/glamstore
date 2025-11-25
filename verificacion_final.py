#!/usr/bin/env python
"""
Script de verificación final del sistema de envío de correos
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

def verificacion_completa():
    """Verificación completa del sistema"""
    print("=== VERIFICACIÓN FINAL DEL SISTEMA ===")
    
    fecha_hoy = timezone.now().date()
    
    # 1. Verificar repartidores
    print("\n1. 📋 VERIFICANDO REPARTIDORES")
    print("-" * 40)
    
    todos_repartidores = Repartidor.objects.all()
    repartidores_con_email = Repartidor.objects.filter(email__isnull=False).exclude(email='')
    
    print(f"Total repartidores: {todos_repartidores.count()}")
    print(f"Con email configurado: {repartidores_con_email.count()}")
    
    for repartidor in todos_repartidores:
        email_status = "✓" if repartidor.email else "✗"
        pedidos_count = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado'],
            fechaCreacion__date=fecha_hoy
        ).count()
        
        pedidos_status = "✓" if pedidos_count > 0 else "✗"
        
        print(f"  {email_status} {pedidos_status} {repartidor.nombreRepartidor}")
        print(f"      Email: {repartidor.email or 'No configurado'}")
        print(f"      Pedidos hoy: {pedidos_count}")
        print()
    
    # 2. Verificar configuración de email
    print("2. 📧 VERIFICANDO CONFIGURACIÓN DE EMAIL")
    print("-" * 40)
    
    from django.conf import settings
    
    config_items = [
        ('EMAIL_BACKEND', getattr(settings, 'EMAIL_BACKEND', 'No configurado')),
        ('EMAIL_HOST', getattr(settings, 'EMAIL_HOST', 'No configurado')),
        ('EMAIL_PORT', getattr(settings, 'EMAIL_PORT', 'No configurado')),
        ('EMAIL_USE_TLS', getattr(settings, 'EMAIL_USE_TLS', 'No configurado')),
        ('EMAIL_HOST_USER', getattr(settings, 'EMAIL_HOST_USER', 'No configurado')),
        ('EMAIL_HOST_PASSWORD', '***configurado***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'No configurado'),
    ]
    
    for key, value in config_items:
        status = "✓" if value != 'No configurado' else "✗"
        print(f"  {status} {key}: {value}")
    
    # 3. Probar envío a cada repartidor con email y pedidos
    print("\n3. 🚀 PROBANDO ENVÍO DE CORREOS")
    print("-" * 40)
    
    repartidores_elegibles = []
    
    for repartidor in repartidores_con_email:
        pedidos_count = Pedido.objects.filter(
            idRepartidor=repartidor,
            estado_pedido__in=['En Camino', 'Confirmado'],
            fechaCreacion__date=fecha_hoy
        ).count()
        
        if pedidos_count > 0:
            repartidores_elegibles.append(repartidor)
    
    print(f"Repartidores elegibles para envío: {len(repartidores_elegibles)}")
    print()
    
    correos_enviados = 0
    errores = 0
    
    for repartidor in repartidores_elegibles:
        print(f"Enviando a: {repartidor.nombreRepartidor} ({repartidor.email})")
        
        try:
            resultado = enviar_correo_repartidor_detallado(repartidor, fecha_hoy)
            if resultado:
                print("  ✅ Enviado exitosamente")
                correos_enviados += 1
            else:
                print("  ❌ Error en el envío")
                errores += 1
        except Exception as e:
            print(f"  ❌ Excepción: {str(e)}")
            errores += 1
        
        print()
    
    # 4. Resumen final
    print("4. 📊 RESUMEN FINAL")
    print("-" * 40)
    print(f"✅ Correos enviados exitosamente: {correos_enviados}")
    print(f"❌ Errores en envío: {errores}")
    print(f"📧 Total repartidores con email: {repartidores_con_email.count()}")
    print(f"📦 Repartidores con pedidos hoy: {len(repartidores_elegibles)}")
    
    if correos_enviados > 0 and errores == 0:
        print("\n🎉 SISTEMA FUNCIONANDO PERFECTAMENTE")
    elif correos_enviados > 0:
        print(f"\n⚠️  SISTEMA FUNCIONANDO CON ALGUNOS ERRORES")
    else:
        print(f"\n❌ SISTEMA CON PROBLEMAS")

def main():
    """Función principal"""
    print("INICIANDO VERIFICACIÓN FINAL")
    print("=" * 50)
    
    verificacion_completa()
    
    print("\nVERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    main()