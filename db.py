from config import create_entry_table_query
import psycopg
import logging


class DB(object):
    def __init__(self, cfg:dict=None, host:str=None, host_port:str=None, user:str=None, password:str=None, db_name:str=None):
        if cfg is None or len(cfg) < 4:
            self._host:str = host
            self._port:str = host_port
            self._user:str = user
            self._password:str = password
            self._db:str = db_name
        else:
            self._host, self._port = cfg["location"].split(':')
            self._user = cfg["credentials"]["user"]
            self._password = cfg["credentials"]["pass"]
            self._db = cfg["db_name"]
        self._conn:psycopg.Connection = None

    def open(self) -> bool:
        try:
            self._conn = psycopg.connect(host=self._host,
                                    user=self._user,
                                    password=self._password,
                                    dbname=self._db,
                                    port=self._port)
        except psycopg.Error:
            logging.error("Could not open DB-Connection")
            return False
        if self._conn.closed:
            logging.error("Could not open DB-Connection")
            return False
        logging.info("Opened DB-Connection")
        return True

    def is_closed(self) -> bool:
        return self._conn.closed

    def close(self) -> bool:
        try:
            self._conn.close()
        except psycopg.Error as e:
            if self._conn.closed:
                logging.info("Closed DB-Connection")
                return True
            logging.error("Could not close DB-Connection: %s", e)
            return False
        logging.info("Closed DB-Connection")
        return True

    def create_tables(self) -> bool:
        if self._conn.closed:
            logging.warning("Could not create tables: Connection not open")
            return False
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(create_entry_table_query)
            self._conn.commit()
        except psycopg.Error as e:
            logging.error("Could not create tables: %s", e)
            return False
        return True

    def upload_data(self, query:str, data:tuple) -> bool:
        if self._conn.closed:
            logging.warning("Could not save data: Connection not open")
            return False
        logging.info("Saving data to DB: %s", data)
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query, data)
            self._conn.commit()
        except psycopg.Error as e:
            logging.error("Could not save data: %s", e)
            return False
        return True

    def upload_data_many(self, query:str, data:list[tuple]) -> bool:
        if self._conn.closed:
            logging.warning("Could not save data: Connection not open")
            return False
        logging.info("Saving data to DB: %s", data)
        try:
            with self._conn.cursor() as cursor:
                #for entry in data:
                    #cursor.execute(query, entry)
                cursor.executemany(query, data)
            self._conn.commit()
        except psycopg.Error as e:
            logging.error("Could not save data: %s", e)
            return False
        return True
