from abc import abstractmethod, ABCMeta
import logging
import requests
import json

class _Sensor(object, metaclass=ABCMeta):

	api_key:str = ""

	def __init__(self, name:str, name_alt:str=None, retro:bool=False, multiple_entries:bool=False) -> None:
		self.name:str = name
		self.name_alt = name if name_alt is None else name_alt
		self.is_retro = retro
		self.enabled:bool = False
		self.sensors:list[str] = []
		self.data = None
		self._multiple_entries = multiple_entries
	
	def has_multiple_entries(self) -> bool:
		return self._multiple_entries
	
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
		return json.loads(response[0])

	@abstractmethod
	def parse_data(self, data:dict) -> dict:
		pass

	@abstractmethod
	def parse_data_tuple(self, data:dict) -> tuple:
		pass

	def load_sensors(self, app:dict) -> None:
		sensors = app.get(self.name)
		if sensors is None:
			return
		self.sensors = sensors

	def enable(self, app:dict) -> None:
		self.enabled = app.get(self.name) is not None
		if len(self.sensors) < 1:
			self.enabled = False
			return
	
	@staticmethod
	def create_header() -> dict:
		if _Sensor.api_key is None:
			raise Exception("API-Key not loaded")
		return {"Authorization":"BEARER " + _Sensor.api_key}
	
	@staticmethod
	def send_request(url:str) -> list:
		timeout = 30 # seconds
		headers = _Sensor.create_header()
		raw = requests.get(url, headers=headers, timeout=timeout)
		as_list = raw.text.splitlines()
		return as_list

	@staticmethod
	def replace_abbreviation(old:str, lookup:dict) -> str:
		"""Replaces the abbreviation of the street with the full
		name of the street. If there could nothing be found, the
		original string is returned.
		"""
		front, back = old.split("-")
		for abbr, name in lookup.items():
			if abbr in back:
				back = back.replace(abbr, name)
				break
		return front + "-" + back

#class CO2(_Sensor):
#	def __init__(self):
#		super().__init__(name="co2")



#class ModbusRaspy(_Sensor):
#	def __init__(self):
#		super().__init__(name="raspi")
