from .sensor import _Sensor

class Meter(_Sensor):
	def __init__(self, retro:bool = False):
		super().__init__(name="sdm230", name_alt="meter", retro=retro)

	def parse_data(self, raw_data: dict) -> dict:
		# sdm230_timestamp, sdm230_name, sdm230_shelter_id,
		# sdm230_kwh, sdm230_frequency, sdm230_voltage, sdm230_rssi
		device_id = raw_data["result"]["end_device_ids"]["device_id"]
		_front, name = device_id.split('-')
		timestamp = raw_data["result"]["received_at"]
		# trim timestamp, as it is too long for the database
		timestamp = timestamp[:timestamp.find('.')+4] + 'Z'

		decoded_payload = raw_data["result"]["uplink_message"]["decoded_payload"]
		rx_metadata = raw_data["result"]["uplink_message"]["rx_metadata"][0]

		app_id = raw_data["result"]["end_device_ids"]["application_ids"]["application_id"]
		shelter_id = app_id[app_id.find('cv')+2:]

		kwh = decoded_payload["kWh"]
		freq = decoded_payload["frequency"]
		volts = decoded_payload["volts"]
		rssi = rx_metadata["rssi"]

		data = {"name":name, "timestamp":timestamp, "shelter_id":shelter_id,
			"kwh":kwh, "frequency":freq, "voltage":volts, "rssi":rssi}
		self.data = data
		return data

	def parse_data_tuple(self, data:dict) -> tuple:
		my_tuple = (data["timestamp"], data["name"], data["shelter_id"],
					data["kwh"], data["frequency"], data["voltage"], data["rssi"])
		return my_tuple
