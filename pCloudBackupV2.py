import os
import subprocess

# Rclone-Konfiguration
remote_name = "pcloud"
# remote_path = "webdav_remote:path"

# Array mit den hochzuladenden Ordnern
folders_to_upload = ["/opt/containers/vaultwarden", "/home/chris/TestUpload"]


def synchronize_folders(folder):
    # Überprüfen, ob der lokale Ordner existiert
    if not os.path.exists(folder):
        print(f'Local folder "{folder}" does not exist. Skipping...')
        return

    # Rclone-Kommando für die Synchronisierung ausführen
    command = f"rclone sync {folder} {remote_name}:{folder} --progress"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    else:
        print("Synchronization completed successfully.")


# Hauptprogramm
for folder in folders_to_upload:
    synchronize_folders(folder)
