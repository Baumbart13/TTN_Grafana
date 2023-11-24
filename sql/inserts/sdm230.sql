INSERT INTO public.sdm230 (
	sdm230_timestamp, sdm230_name, sdm230_shelter_id, sdm230_kwh, sdm230_frequency, sdm230_voltage, sdm230_rssi
) VALUES (
	%s, %s, %s, %s, %s, %s, %s
)ON CONFLICT (sdm230_timestamp, sdm230_name) DO NOTHING;