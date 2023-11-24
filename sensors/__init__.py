from .sensor import _Sensor
from .Meter import Meter
from .Raspi import Raspi

def reset_sensor_collection() -> list[_Sensor]:
	return[
		Meter(retro=True),
		Raspi()
		]

sensor_collection:list[_Sensor] = reset_sensor_collection()