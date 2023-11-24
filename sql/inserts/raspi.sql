INSERT INTO public.raspi (
	raspi_timestamp, raspi_shelter_id, raspi_meter_name, raspi_kwh, raspi_rssi
) VALUES (
	%s, %s, %s, %s, %s
) ON CONFLICT (raspi_timestamp, raspi_shelter_id, raspi_meter_name) DO NOTHING;