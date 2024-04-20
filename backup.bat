SET PGPASSWORD={DB_PASSWORD}
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -U {DB_USER} --inserts -d ttn_grafana -t sdm230 -f "{BACKUP_OUTPUT_DATA}\TTN_Grafana_Interface\sdm230_data.sql" > "{LOGDIR}\backup.sdm230.log"
"C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" -U {DB_USER} --inserts -d ttn_grafana -t raspi -f "{BACKUP_OUTPUT_DATA}\TTN_Grafana_Interface\raspi_data.sql" > "{LOGDIR}\backup.raspi.log"
