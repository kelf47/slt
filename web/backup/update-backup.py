import dropbox
from dropbox.files import WriteMode
import os

auth_token = "buLoD3InxtAAAAAAAAAAFLqXVfilxYOZKT86oHz9nCEsVOA9a667Si6kzLFyKGIR"
client = dropbox.DropboxClient(auth_token)

# Get all old backups in folder
file_response = client.files_list_folder("")
old_backups = []
if file_response:
    old_backups = [entry.path_lower for entry in file_response.entries]

# Upload the new backup file
for i in os.listdir("/tmp"):
    if os.path.isfile(os.path.join("/tmp", i)) and 'slt-backup' in i:
        with open("/tmp/{}".format(i), 'rb') as f:
            client.files_upload(f.read(), "/{}".format(i), mode=WriteMode(
                'overwrite'))
        print('uploaded')
        break

# Delete old backups
for backup in old_backups:
    client.files_delete(backup)
