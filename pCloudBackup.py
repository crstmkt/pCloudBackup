import os
import hashlib
import datetime
from webdav3.client import Client

# from webdav3.client import

# WebDAV-Server Konfiguration
options = {
    "webdav_hostname": "https://ewebdav.pcloud.com:443",
    "webdav_login": "user@mail.com",
    "webdav_password": "A5tr0nGPa55Word",
    "verbose": "True",
}

# Array mit den hochzuladenden Ordnern
folders_to_upload = [
    "/home/user/Downloads/extracted",
]


def create_remote_root_folder(client, remote_folder):
    if not client.check(remote_folder):
        # Aufteilung des Pfads in Verzeichnisse
        directories = remote_folder.strip("/").split("/")
        current_path = ""
        for directory in directories:
            current_path += f"/{directory}"
            if not client.check(current_path):
                try:
                    client.mkdir(current_path)
                    print(f"Erstellt: {current_path}")
                except:
                    # Übergeordneten Ordner erstellen und erneut versuchen
                    create_remote_root_folder(client, current_path)
                    client.mkdir(current_path)
                    print(f"Erstellt: {current_path}")


def create_remote_subfolder(client, remote_path, remote_folder):
    if not client.check(remote_path + "/" + remote_folder):
        client.mkdir(remote_path + "/" + remote_folder)
        print(f"Erstellt: {remote_path}/{remote_folder}")
    else:
        print(f"{remote_path}/{remote_folder} already exists. Skipping...")


def precheck_file(client, remote_path, file):
    # Dateiinfo abrufen
    local_file = os.path.join(remote_path + "/" + file.name)
    if not client.check(local_file):
        upload_file(client, local_file)
        print(f"Hochgeladen: {local_file}")


def recursive_directory_walk(client, remote_path):
    entries = os.scandir(remote_path)
    for entry in entries:
        if entry.is_dir():
            create_remote_subfolder(client, remote_path, entry.name)
            recursive_directory_walk(client, remote_path + "/" + entry.name)
        elif entry.is_file():
            precheck_file(client, remote_path, entry)


def syncronize_folders(client, local_path):
    # Überprüfen, ob der lokale Ordner existiert
    if not os.path.exists(local_path):
        print(f'Lokaler Ordner "{local_path}" existiert nicht.')
        return

    # Remote Root-Folder Ordnerstruktur aufbauen
    create_remote_root_folder(client, local_path)

    # Remote Subfolder Struktur aufbauen
    recursive_directory_walk(client, local_path)


def upload_file(client, local_file):
    remote_file = local_file
    print(f"Starte Upload: {local_file}")
    client.upload_sync(local_file, remote_file)


# def upload_folder(client, local_path, remote_path):
#     # Überprüfen, ob der lokale Ordner existiert
#     if not os.path.exists(local_path):
#         print(f'Lokaler Ordner "{local_path}" existiert nicht.')
#         return

#     # Dateien im lokalen Ordner auflisten
#     for root, dirs, files in os.walk(local_path):
#         # Remote-Ordnerstruktur aufbauen
#         remote_folder = local_path
#         create_remote_folder(client, remote_folder)

#         for dir in dirs:
#             remote_folder = local_path + "/" + dir
#             create_remote_folder(client, remote_folder)

#         # Dateien hochladen
#         for file in files:
#             local_file_path = os.path.join(root, file)
#             remote_file_path = remote_folder + "/" + file

#             # Überprüfen, ob die Datei bereits auf dem Server existiert und unverändert ist
#             if client.check(remote_file_path):
#                 remote_file_info = client.info(remote_file_path)
#                 local_last_modified = datetime.datetime.fromtimestamp(
#                     os.path.getmtime(local_file_path)
#                 )
#                 remote_last_modified = datetime.datetime.strptime(
#                     remote_file_info["modified"], "%a, %d %b %Y %H:%M:%S %Z"
#                 )
#                 local_crc = hashlib.md5(open(local_file_path, "rb").read()).hexdigest()
#                 remote_crc = remote_file_info["etag"].replace('"', "")

#                 # Datei hochladen, wenn sie neuer oder verändert ist
#                 if (
#                     local_last_modified > remote_last_modified
#                     or local_crc != remote_crc
#                 ):
#                     client.upload(remote_file_path, local_file_path)
#                     print(f"Hochgeladen: {local_file_path}")
#                 else:
#                     print(
#                         f"Übersprungen: {local_file_path} (bereits auf dem Server vorhanden)"
#                     )
#             else:
#                 client.upload(remote_file_path, local_file_path)
#                 print(f"Hochgeladen: {local_file_path}")


# Hauptprogramm
client = Client(options)
client.verify = True  # Falls Sie ein selbstsigniertes SSL-Zertifikat verwenden
for folder in folders_to_upload:
    syncronize_folders(client, folder)
