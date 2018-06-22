_now=$(date +"%m_%d_%Y")
rm /tmp/slt-backup*
PGPASSWORD="postgres" pg_dump -h postgres -p 5432 -U postgres postgres > /tmp/slt-backup-$_now.sql
/usr/local/bin/python /usr/src/app/backup/update-backup.py
