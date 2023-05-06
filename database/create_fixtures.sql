CREATE TABLE IF NOT EXISTS half_hour(
	price_id SERIAL PRIMARY KEY,
	date_price TIMESTAMP,
	open_price DECIMAL,
	high_price DECIMAL,
	low_price DECIMAL,
	close_price DECIMAL,
	volume DECIMAL
);
CREATE TABLE IF NOT EXISTS four_hours(
	price_id SERIAL PRIMARY KEY,
	date_price TIMESTAMP,
	open_price DECIMAL,
	high_price DECIMAL,
	low_price DECIMAL,
	close_price DECIMAL,
	volume DECIMAL
);
CREATE TABLE IF NOT EXISTS four_days(
	price_id SERIAL PRIMARY KEY,
	date_price TIMESTAMP,
	open_price DECIMAL,
	high_price DECIMAL,
	low_price DECIMAL,
	close_price DECIMAL,
	volume DECIMAL
);
