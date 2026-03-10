import os

def get_folder_size(folder_path):
    """Calcule la taille totale d'un dossier en octets."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Ignorer les liens symboliques et les fichiers inaccessibles
            if not os.path.islink(filepath):
                try:
                    total_size += os.path.getsize(filepath)
                except (FileNotFoundError, PermissionError):
                    pass
    return total_size

def format_size(size_bytes):
    """Formate la taille en Mo ou Go."""
    if size_bytes == 0:
        return "0 Mo"
    
    size_mb = size_bytes / (1024 ** 2)
    size_gb = size_bytes / (1024 ** 3)
    
    if size_gb >= 1:
        return f"{size_gb:.2f} Go"
    else:
        return f"{size_mb:.2f} Mo"

if __name__ == "__main__":
    folder_path = r"D:\kylian\Pictures"
    
    # Vérifier si le dossier existe
    if not os.path.exists(folder_path):
        print(f"Erreur : Le dossier '{folder_path}' n'existe pas.")
    elif not os.path.isdir(folder_path):
        print(f"Erreur : '{folder_path}' n'est pas un dossier.")
    else:
        size_bytes = get_folder_size(folder_path)
        formatted_size = format_size(size_bytes)
        print(f"Taille du dossier {folder_path} : {formatted_size}")
