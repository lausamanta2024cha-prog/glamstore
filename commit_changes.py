#!/usr/bin/env python
import subprocess
import sys

try:
    subprocess.run(['git', 'add', 'core/models/pedidos.py', 'core/Gestion_admin/views.py'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Fix repartidores view: Remove Count annotation to fix 500 error'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print("Commit and push successful!")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)
