#!/usr/bin/env python
"""
Script para verificar que el formulario HTML está correcto
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glamstore.settings')
django.setup()

from django.test import Client
from core.models.repartidores import Repartidor

def test_formulario():
    """Prueba el formulario HTML"""
    print("=== VERIFICANDO FORMULARIO HTML ===")
    
    # Crear cliente de prueba
    client = Client()
    
    # Obtener la página de repartidores
    print("📄 Obteniendo página de repartidores...")
    response = client.get('/gestion/repartidores/')
    
    if response.status_code != 200:
        print(f"❌ Error: Status code {response.status_code}")
        return
    
    print(f"✅ Página cargada correctamente (Status: {response.status_code})")
    
    # Verificar que el formulario existe
    html_content = response.content.decode('utf-8')
    
    if 'formEnvioRepartidores' not in html_content:
        print("❌ Formulario no encontrado en HTML")
        return
    
    print("✅ Formulario encontrado")
    
    if 'repartidor_ids' not in html_content:
        print("❌ Checkboxes no encontrados en HTML")
        return
    
    print("✅ Checkboxes encontrados")
    
    if 'enviar_correos_repartidores_seleccionados' not in html_content:
        print("❌ URL de envío no encontrada")
        return
    
    print("✅ URL de envío encontrada")
    
    # Contar checkboxes
    checkbox_count = html_content.count('name="repartidor_ids"')
    print(f"✅ Checkboxes encontrados: {checkbox_count}")
    
    # Obtener repartidores
    repartidores = Repartidor.objects.all()
    print(f"✅ Repartidores en BD: {repartidores.count()}")
    
    if checkbox_count != repartidores.count():
        print(f"⚠️  Advertencia: Checkboxes ({checkbox_count}) != Repartidores ({repartidores.count()})")
    else:
        print(f"✅ Cantidad de checkboxes coincide con repartidores")
    
    # Verificar estructura del formulario
    print("\n📋 Verificando estructura del formulario...")
    
    if '<form method="POST" action="/gestion/repartidores/enviar_correos_seleccionados/"' in html_content:
        print("✅ Método POST correcto")
    else:
        print("❌ Método POST incorrecto")
    
    if 'csrf_token' in html_content:
        print("✅ Token CSRF presente")
    else:
        print("❌ Token CSRF no encontrado")
    
    print("\n✅ FORMULARIO HTML VERIFICADO CORRECTAMENTE")

def main():
    """Función principal"""
    print("INICIANDO VERIFICACIÓN DE FORMULARIO HTML")
    print("=" * 50)
    
    test_formulario()
    
    print("\nVERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    main()