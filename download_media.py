#!/usr/bin/env python
"""
Script para descargar archivos media desde GitHub durante el build en Render
"""
import os
import urllib.request
from pathlib import Path

# URL base del repositorio en GitHub (raw content)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/lausamanta2024cha-prog/glamstore/main"

# Carpetas de media a descargar
MEDIA_FOLDERS = [
    'media/categorias',
    'media/productos',
]

def download_media_files():
    """Descarga todos los archivos media desde GitHub"""
    print("Descargando archivos media desde GitHub...")
    
    for folder in MEDIA_FOLDERS:
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Lista de archivos conocidos en cada carpeta
        if folder == 'media/categorias':
            files = [
                'accessories_feb_main.jpg',
                'cuidado_facial.jpg',
                'cuidado_facial_T4konPk.jpg',
                'la.jpg',
                'ojos.jpg',
                'rostro.avif',
                'uñas.webp',
            ]
        elif folder == 'media/productos':
            files = [
                'balsamo.webp',
                'base_polvo_OZcGSIu.webp',
                'base_polvo.webp',
                'base.png',
                'br.webp',
                'bronceador.jpg',
                'corrector.avif',
                'dd.webp',
                'delini.webp',
                'es.jpg',
                'esm.webp',
                'esp.webp',
                'ess.webp',
                'ilumi_p.webp',
                'iluminador.webp',
                'ki.webp',
                'l.webp',
                'la.webp',
                'll.webp',
                'o.webp',
                'otra_b.webp',
                'p.webp',
                'pestanina.webp',
                'pinta_cejaz.avif',
                'pinzas.webp',
                'red_velved.jpg',
                'rubor.jpg',
                's.jpg',
                'top.jpg',
                'tr.webp',
            ]
        else:
            files = []
        
        for filename in files:
            file_path = folder_path / filename
            
            # Saltar si ya existe
            if file_path.exists():
                print(f"  [OK] {file_path} ya existe")
                continue
            
            # Descargar desde GitHub
            url = f"{GITHUB_BASE_URL}/{folder}/{filename}"
            try:
                print(f"  Descargando {filename}...")
                urllib.request.urlretrieve(url, str(file_path))
                print(f"  [OK] {filename} descargado")
            except Exception as e:
                print(f"  [ERROR] No se pudo descargar {filename}: {e}")

if __name__ == '__main__':
    download_media_files()
    print("\n[OK] Descarga de archivos media completada")
