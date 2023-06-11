CREATE TABLE IF NOT EXISTS assets(
	coin_id TEXT PRIMARY KEY,
	symbol TEXT NOT NULL
);

INSERT INTO assets (coin_id, symbol)
VALUES
	('bitcoin', 'BTC'),
	('ethereum', 'ETH'),
	('ripple', 'XRP'),
	('matic-network', 'MATIC'),
	('polkadot', 'DOT');

CREATE TABLE IF NOT EXISTS half_hours(
	price_id INT GENERATED ALWAYS AS IDENTITY,
	date_price TIMESTAMP,
	open DECIMAL,
	high DECIMAL,
	low DECIMAL,
	close DECIMAL,
	volume DECIMAL,
	--coin_id TEXT NOT NULL,
	--PRIMARY KEY (price_id),
	--CONSTRAINT fk_coin_id 
		--FOREIGN KEY (coin_id)
			--REFERENCES assets(coin_id)
);

CREATE TABLE IF NOT EXISTS four_hours(
	price_id INT GENERATED ALWAYS AS IDENTITY,
	date_price TIMESTAMP,
	open DECIMAL,
	high DECIMAL,
	low DECIMAL,
	close DECIMAL,
	volume DECIMAL,
	coin_id TEXT NOT NULL,
	--PRIMARY KEY (price_id),
	--CONSTRAINT fk_coin_id 
		--FOREIGN KEY (coin_id)
			--REFERENCES assets(coin_id)
);


CREATE TABLE IF NOT EXISTS four_days(
	price_id INT GENERATED ALWAYS AS IDENTITY,
	date_price TIMESTAMP,
	open DECIMAL,
	high DECIMAL,
	low DECIMAL,
	close DECIMAL,
	volume DECIMAL,
	--coin_id TEXT NOT NULL,
	--PRIMARY KEY (price_id),
	--CONSTRAINT fk_coin_id 
		--FOREIGN KEY (coin_id)
			--REFERENCES assets(coin_id)
);
