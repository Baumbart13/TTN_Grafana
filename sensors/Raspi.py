from .sensor import _Sensor
import json
import logging


class Raspi(_Sensor):
	def __init__(self, retro:bool = False):
		super().__init__(name="raspi", name_alt="raspi", retro=retro, multiple_entries=True)
	
	def retrieve_data(self, app_name:str, app:dict, url:str, sensor_name:str) -> dict:
		full_sensor_name = self.name_alt + '-' + sensor_name if self.is_retro else self.name + '-' + sensor_name
		response = _Sensor.send_request(url.format(app=app_name, sensor=full_sensor_name))
		if len(response) < 1:
			return {}
		if "error" in response[-1][:10]:
			err = json.loads(response[-1])
			err_code = err["error"]["code"]
			err_msg = err["error"]["message"]
			logging.error('Unsuccessful response. Code %s, "%s"', err_code, err_msg)
		response.reverse()
		for i in range(len(response)):
			response[i] = json.loads(response[i])
		return response

	def parse_data(self, raw_data: dict) -> dict:
		entries:list[dict] = []
		for res in raw_data:
			timestamp:str = res["result"]["received_at"]
			# trim timestamp, as it is too long for the database
			timestamp = timestamp[:timestamp.find('.')+4] + 'Z'

			decoded_payload = res["result"]["uplink_message"]["decoded_payload"]["meters"]
			rx_metadata = res["result"]["uplink_message"]["rx_metadata"][0]

			app_id = res["result"]["end_device_ids"]["application_ids"]["application_id"]
			shelter_id = int(app_id[app_id.find('cv')+2:])

			rssi = rx_metadata["rssi"]

			for entry in decoded_payload:
				kwh = entry["count"]
				data = {"timestamp":timestamp, "shelter_id":shelter_id, "meter_name":entry["name"],
						"count":kwh, "rssi":rssi}
				entries.append(data)

		return entries

	def parse_data_tuple(self, data:dict) -> list:
			#raspi_timestamp, raspi_shelter_id, raspi_meter_name, raspi_kwh, raspi_rssi
		big_coll:list = []
		for entry in data:
			my_tuple = (entry["timestamp"], entry["shelter_id"], entry["meter_name"],
						entry["count"], entry["rssi"])
			big_coll.append(my_tuple)
			
		return big_coll
