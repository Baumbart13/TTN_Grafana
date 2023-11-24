from config import api_url
from sensors import _Sensor
from db import DB
import sensors
import config
import logging

configuration = config.config


def main2():
    apps:list = configuration["ttn"]["applications"][0]
    db_creds = configuration["database"]
    db = DB(db_creds)
    for _ in range(db_creds["connection_retries"]):
        if db.open():
            break
    if db.is_closed():
        logging.critical("""Could not connect to DB after %s tries. No tables created. Aborting""", db_creds["connection_retries"])
        return
    db.create_tables()
    db.close()
    for app_name, app in apps.items():
        sensors.reset_sensor_collection()

        _Sensor.api_key = app["api-key"]
        for sensor_type in sensors.sensor_collection:
            sensor_type:_Sensor
            sensor_type.load_sensors(app)
            sensor_type.enable(app)
            if not sensor_type.enabled:
                continue
            
            tuple_values:list[tuple] = []
            for sensor in sensor_type.sensors:
                sensor:str
                data = sensor_type.retrieve_data(app_name, app, api_url, sensor)
                if len(data) < 1:
                    logging.warning("Empty response for '%s', '%s'", app_name, sensor_type.name + '-' + sensor)
                    continue
                data_extract = sensor_type.parse_data(data)
                data_tuple = sensor_type.parse_data_tuple(data_extract)
                if isinstance(data_tuple, list):
                    tuple_values.extend(data_tuple)
                else:
                    tuple_values.append(data_tuple)
            sql:str = config.insertion_queries[sensor_type.name]
            for _ in range(db_creds["connection_retries"]):
                if db.open():
                    break
            if db.is_closed():
                logging.error("""Could not save data after %s tries. Data not saved.
                              Continuing with next sensor-type""", db_creds["connection_retries"])
            #for val in tuple_values:
                #db.upload_data(sql, val)
            if db.upload_data_many(sql, tuple_values):
                logging.info("Data saved to DB succesfully")
            db.close()

if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", datefmt='%m/%d/%YT%I:%M:%S', force=True)
    logging.root.setLevel(logging.DEBUG)
    logging.root.name = "espo_ttn"
    main2()