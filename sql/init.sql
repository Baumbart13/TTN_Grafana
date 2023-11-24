DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = 'DATABASE_NAME') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE DATABASE_NAME');
   END IF;
END
$do$;

DO $$
BEGIN
   IF NOT EXISTS (
      SELECT 1
      FROM information_schema.tables
      WHERE table_name = 'sdm230'
   ) THEN
      RAISE NOTICE 'Table sdm230 does not exist. Creating it now.';

      CREATE TABLE public.sdm230
      (
         sdm230_timestamp TIMESTAMP WITH TIME ZONE,
         sdm230_name VARCHAR(10),
         sdm230_shelter_id SMALLINT,
         sdm230_kwh NUMERIC(9, 4),
         sdm230_frequency DOUBLE PRECISION,
         sdm230_voltage DOUBLE PRECISION,
         sdm230_rssi DOUBLE PRECISION,
         CONSTRAINT sdm230_pk PRIMARY KEY (sdm230_timestamp, sdm230_name)
      );
      ALTER TABLE IF EXISTS public.sdm230 OWNER TO dev;
      COMMENT ON TABLE public.sdm230 IS 'Electrical meter Eastron SDM230';
   END IF;
END $$;

DO $$
BEGIN
   IF NOT EXISTS (
      SELECT 1
      FROM information_schema.tables
      WHERE table_name = 'raspi'
   ) THEN
      RAISE NOTICE 'Table raspi does not exist. Creating it now.';

      CREATE TABLE public.raspi
      (
         raspi_timestamp TIMESTAMP WITH TIME ZONE,
         raspi_shelter_id SMALLINT,
         raspi_meter_name VARCHAR(10),
         raspi_kwh NUMERIC(10, 4),
         raspi_rssi DOUBLE PRECISION,
         CONSTRAINT raspi_pk PRIMARY KEY (raspi_timestamp, raspi_shelter_id, raspi_meter_name)
      );
      ALTER TABLE IF EXISTS public.raspi OWNER TO dev;

      COMMENT ON TABLE public.raspi IS 'Electrical meters read by a Raspberry Pi via Modbus';
   END IF;
END $$;
