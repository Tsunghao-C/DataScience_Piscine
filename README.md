# DataScience_Piscine
DataScience Piscine from school 42. Mainly about Data engineering, Analysis, and Model Training

# Notes about SQL commands

1. Create a new table and set columns

-- Table: public.events

-- DROP TABLE IF EXISTS public.events;

CREATE TABLE IF NOT EXISTS public.data_2022_dec
(
    event_time timestamp with time zone,
    event_type text COLLATE pg_catalog."default",
    product_id bigint,
    price numeric(10,2),
    user_id bigint,
    user_session uuid
);

2. Copy data using psql
```
COPY data_2022_dec(event_time, event_type, product_id, price, user_id, user_session)
FROM '/tmp/data_2022_dec.csv'
DELIMITER ','
CSV HEADER;
```

3. Go to table and use SQL to view data

```
SELECT * FROM events LIMIT 20
```