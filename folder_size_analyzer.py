#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyseur de taille de dossier avancé.
Calcule la taille des dossiers, affiche les détails par sous-dossier et par type de fichier.
"""

import os
import sys
from collections import defaultdict
from datetime import datetime

def get_folder_size(folder_path):
    """
    Calcule la taille totale d'un dossier en octets.
    
    Args:
        folder_path (str): Chemin du dossier à analyser.
        
    Returns:
        int: Taille totale en octets.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if not os.path.islink(filepath) and os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)
            except (FileNotFoundError, PermissionError, OSError):
                continue
    return total_size

def get_subfolder_sizes(folder_path):
    """
    Calcule la taille de chaque sous-dossier direct.
    
    Args:
        folder_path (str): Chemin du dossier parent.
        
    Returns:
        dict: Dictionnaire {nom_sous_dossier: taille_en_octets}.
    """
    subfolder_sizes = {}
    try:
        entries = os.listdir(folder_path)
    except PermissionError:
        return subfolder_sizes
        
    for entry in entries:
        entry_path = os.path.join(folder_path, entry)
        if os.path.isdir(entry_path) and not os.path.islink(entry_path):
            subfolder_sizes[entry] = get_folder_size(entry_path)
    return subfolder_sizes

def get_file_type_distribution(folder_path):
    """
    Analyse la répartition des fichiers par extension.
    
    Args:
        folder_path (str): Chemin du dossier à analyser.
        
    Returns:
        dict: Dictionnaire {extension: {'count': nb, 'size': taille_octets}}.
    """
    distribution = defaultdict(lambda: {'count': 0, 'size': 0})
    
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if not os.path.islink(filepath) and os.path.isfile(filepath):
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower() if ext else "(sans extension)"
                    size = os.path.getsize(filepath)
                    distribution[ext]['count'] += 1
                    distribution[ext]['size'] += size
            except (FileNotFoundError, PermissionError, OSError):
                continue
                
    return dict(distribution)

def get_largest_files(folder_path, top_n=10):
    """
    Trouve les N plus gros fichiers du dossier.
    
    Args:
        folder_path (str): Chemin du dossier à analyser.
        top_n (int): Nombre de fichiers à retourner.
        
    Returns:
        list: Liste de tuples (chemin_relief, taille_octets).
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if not os.path.islink(filepath) and os.path.isfile(filepath):
                    size = os.path.getsize(filepath)
                    rel_path = os.path.relpath(filepath, folder_path)
                    files.append((rel_path, size))
            except (FileNotFoundError, PermissionError, OSError):
                continue
    
    files.sort(key=lambda x: x[1], reverse=True)
    return files[:top_n]

def format_size(size_bytes):
    """
    Formate la taille en une chaîne lisible (Mo ou Go).
    
    Args:
        size_bytes (int): Taille en octets.
        
    Returns:
        str: Taille formatée.
    """
    if size_bytes == 0:
        return "0 Mo"
    
    size_mb = size_bytes / (1024 ** 2)
    size_gb = size_bytes / (1024 ** 3)
    
    if size_gb >= 1:
        return f"{size_gb:.2f} Go"
    else:
        return f"{size_mb:.2f} Mo"

def print_report(folder_path):
    """
    Affiche un rapport complet sur le dossier.
    
    Args:
        folder_path (str): Chemin du dossier à analyser.
    """
    print("=" * 60)
    print(f"RAPPORT D'ANALYSE : {folder_path}")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Taille totale
    total_size = get_folder_size(folder_path)
    print(f"\n📁 TAILLE TOTALE : {format_size(total_size)}")
    
    # Sous-dossiers
    subfolder_sizes = get_subfolder_sizes(folder_path)
    if subfolder_sizes:
        print("\n📂 DÉTAIL PAR SOUS-DOSSIER :")
        sorted_subfolders = sorted(subfolder_sizes.items(), key=lambda x: x[1], reverse=True)
        for name, size in sorted_subfolders:
            percentage = (size / total_size * 100) if total_size > 0 else 0
            print(f"   - {name}: {format_size(size)} ({percentage:.1f}%)")
    
    # Distribution par type
    file_types = get_file_type_distribution(folder_path)
    if file_types:
        print("\n📊 DISTRIBUTION PAR TYPE DE FICHIER :")
        sorted_types = sorted(file_types.items(), key=lambda x: x[1]['size'], reverse=True)
        for ext, data in sorted_types[:10]:  # Top 10 types
            percentage = (data['size'] / total_size * 100) if total_size > 0 else 0
            print(f"   - {ext}: {data['count']} fichiers, {format_size(data['size'])} ({percentage:.1f}%)")
    
    # Plus gros fichiers
    largest_files = get_largest_files(folder_path, top_n=5)
    if largest_files:
        print("\n🔝 TOP 5 DES PLUS GROS FICHIERS :")
        for i, (filepath, size) in enumerate(largest_files, 1):
            print(f"   {i}. {filepath} - {format_size(size)}")
    
    print("\n" + "=" * 60)

def main():
    """Fonction principale."""
    # Chemin par défaut
    default_path = r"D:\kylian\Pictures"
    
    # Utilisation d'un argument en ligne de commande si fourni
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = default_path
    
    # Vérifications
    if not os.path.exists(folder_path):
        print(f"❌ Erreur : Le dossier '{folder_path}' n'existe pas.")
        sys.exit(1)
    
    if not os.path.isdir(folder_path):
        print(f"❌ Erreur : '{folder_path}' n'est pas un dossier.")
        sys.exit(1)
    
    # Génération du rapport
    try:
        print_report(folder_path)
    except KeyboardInterrupt:
        print("\n\n⚠️  Analyse interrompue par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur lors de l'analyse : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
