#!/usr/local/bin/python

import dropbox
import os

CHUNK_SIZE = 4 * 1024 * 1024
auth_token = "buLoD3InxtAAAAAAAAAAFLqXVfilxYOZKT86oHz9nCEsVOA9a667Si6kzLFyKGIR"
client = dropbox.Dropbox(auth_token)

# Get all old backups in folder
file_response = client.files_list_folder("")
old_backups = []
if file_response:
    old_backups = [entry.path_lower for entry in file_response.entries]

# Upload the new backup file
for i in os.listdir("/tmp"):
    if os.path.isfile(os.path.join("/tmp", i)) and 'slt-backup' in i:
        f = open("/tmp/{}".format(i), 'rb')
        file_size = os.path.getsize("/tmp/{}".format(i))
        print("file_size: {}  max_size: {}".format(file_size, CHUNK_SIZE))
        if file_size <= CHUNK_SIZE:
            res = client.files_upload(f, "/{}".format(i))
            print(res)
        else:
            upload_session_start_result = client.files_upload_session_start(
                f.read(CHUNK_SIZE))
            cursor = dropbox.files.UploadSessionCursor(
                session_id=upload_session_start_result.session_id,
                offset=f.tell())
            commit = dropbox.files.CommitInfo(path="/{}".format(i))

            while f.tell() < file_size:
                if ((file_size - f.tell()) <= CHUNK_SIZE):
                    res = client.files_upload_session_finish(
                        f.read(CHUNK_SIZE), cursor, commit)
                    print(res)
                else:
                    client.files_upload_session_append(f.read(CHUNK_SIZE),
                                                       cursor.session_id,
                                                       cursor.offset)
                    cursor.offset = f.tell()
        f.close()
        os.remove("/tmp/{}".format(i))

# Delete old backups
for backup in old_backups:
    client.files_delete(backup)
