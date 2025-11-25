#!/usr/bin/env python
"""
Script para crear la migración y aplicarla
"""
import os
import subprocess

os.chdir('/ProyectoF/glamstore')

# Crear migración
print("Creando migración...")
subprocess.run(['python', 'manage.py', 'makemigrations', 'core'], check=True)

# Aplicar migración
print("Aplicando migración...")
subprocess.run(['python', 'manage.py', 'migrate'], check=True)

print("✅ Migración completada")
