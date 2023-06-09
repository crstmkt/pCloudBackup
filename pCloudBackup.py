import os
import hashlib
import datetime
from webdav3.client import Client

# WebDAV-Server Konfiguration
server_url = "https://ewebdav.pcloud.com:443"
username = ""
password = ""

# Array mit den hochzuladenden Ordnern
folders_to_upload = [
    "/home/user/Downloads/extracted",
]


def upload_folder(client, local_path, remote_path):
    # Überprüfen, ob der lokale Ordner existiert
    if not os.path.exists(local_path):
        print(f'Lokaler Ordner "{local_path}" existiert nicht.')
        return

    # Dateien im lokalen Ordner auflisten
    for root, dirs, files in os.walk(local_path):
        # Remote-Ordnerstruktur aufbauen
        remote_folder = remote_path + root.replace(local_path, "").replace("\\", "/")
        client.mkdir(remote_folder, safe=True)

        # Dateien hochladen
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = remote_folder + "/" + file

            # Überprüfen, ob die Datei bereits auf dem Server existiert und unverändert ist
            if client.check(remote_file_path):
                remote_file_info = client.info(remote_file_path)
                local_last_modified = datetime.datetime.fromtimestamp(
                    os.path.getmtime(local_file_path)
                )
                remote_last_modified = datetime.datetime.strptime(
                    remote_file_info["modified"], "%a, %d %b %Y %H:%M:%S %Z"
                )
                local_crc = hashlib.md5(open(local_file_path, "rb").read()).hexdigest()
                remote_crc = remote_file_info["etag"].replace('"', "")

                # Datei hochladen, wenn sie neuer oder verändert ist
                if (
                    local_last_modified > remote_last_modified
                    or local_crc != remote_crc
                ):
                    client.upload(remote_file_path, local_file_path, True)
                    print(f"Hochgeladen: {local_file_path}")
                else:
                    print(
                        f"Übersprungen: {local_file_path} (bereits auf dem Server vorhanden)"
                    )
            else:
                client.upload(remote_file_path, local_file_path, True)
                print(f"Hochgeladen: {local_file_path}")


# Hauptprogramm
with Client(server_url, username, password) as client:
    for folder in folders_to_upload:
        upload_folder(client, folder, "")
