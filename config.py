import json
import os
import logging

def load_config(path:str="./config.json") -> dict:
	logging.debug("Fetching config")
	conf:dict = None
	with open(path, 'r', encoding="utf-8") as inFile:
		conf = json.load(inFile)
	return conf

def load_init_sql(path:str="./sql/init.sql") -> str:
	logging.debug("Fetching initialization SQL")
	sql:str = None
	with open(path) as f:
		sql = f.read().replace("DATABASE_NAME", config["database"]["db_name"])
	return sql

def load_insertion_sql(path:str="./sql/inserts") -> dict:
	logging.debug("Fetching SQL-Inserts")
	d:dict = {}
	for curr_path, _dirs, files in os.walk(path):
		for file in files:
			n = os.path.join(curr_path, file)
			n = os.path.abspath(n)
			name:str = file.replace(".sql", "")
			logging.debug("Fetching SQL-Insert for '%s'", name)
			contents_stripped:str = None
			with open(n) as f:
				contents = f.read().replace("\n", "")
				contents_stripped = contents.replace("\t", " ")
			logging.debug("Succesfully fetched SQL-Insert for '%s'", name)
			d[name] = contents_stripped
	return d

config:dict = load_config()
create_entry_table_query:str = load_init_sql()
insertion_queries:dict = load_insertion_sql()
api_url:str = "https://eu1.cloud.thethings.network/api/v3/as/applications/{app}/devices/{sensor}/packages/storage/uplink_message"
