import pandas as pd
import requests
import time

from datetime import datetime
from sqlalchemy import text, Table, MetaData, create_engine
from sqlalchemy.exc import NoSuchTableError


def fetch_data_from_api(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError('Failed to get data from the API')


def get_ohcl(coin_id, vs_currency, days):

    """Returns a Pandas DataFrame with timestamp, open, high, low, close data

    Parameters

    coin_id : str
        coin_id of the coin in CoinGecko's API
    vs_currency : str
        The target currency of market data (usd, eur, jpy, etc.)
    days : str
        Data up to number of days ago (1/30/max)

    Candle's body:

    1 day: 30 minutes
    30 days: 4 hours
    max: 4 days
    """

    historical_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency={vs_currency}&days={days}'
    historical_data = fetch_data_from_api(historical_url)

    historical_df = pd.DataFrame(historical_data)
    historical_df.rename(columns={0: 'unix_timestamp', 1: 'open',
                                  2: 'high', 3: 'low', 4: 'close'}, inplace=True)

    return historical_df


def get_volume(coin_id, vs_currency, days):

    """Returns a Pandas DataFrame with timestamp, volume data

    Parameters

    coin_id : str
        coin_id of the coin in CoinGecko's API
    vs_currency : str
        The target currency of market data (usd, eur, jpy, etc.)
    days : str
        Data up to number of days ago (1/30/max)

    Candle's body:

    1 day from current time = 5 minute interval data
    30 days from current time = hourly data
    max = daily data (00:00 UTC)"""

    volume_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}"
    volume_data = fetch_data_from_api(volume_url)

    volume_df = pd.DataFrame(volume_data)
    volume_df = pd.DataFrame(volume_df['total_volumes'].to_list(), columns=['unix_timestamp', 'volume'])

    return volume_df


def convert_timestamp(df):

    """Converts the Unix Timestamp to a more readable format, namely YYYY-MM-DD HH:MM:SS

    Parameters

    df : pandas.core.frame.DataFrame"""

    df['date_price'] = df['unix_timestamp'].apply(
        lambda a: (a / 1000.0) - ((a / 1000.0) % (30 * 60))  # Converts milliseconds to seconds and subtracts the
        # difference between the time the record was taken, and the closest half hour
    ).apply(lambda b: datetime.fromtimestamp(b))  # Converts the adjusted timestamp using Python's datetime library
    df = df.drop(columns=['unix_timestamp'])  # Drops the unix_timestamp column to avoid duplicates
    return df


def pull_coin_data(coin_id, vs_currency, days):

    """Returns a single DataFrame containing the OHLC prices, volume, and timestamps
    for the given coin, vs_currency and timeframe (days)

    Parameters:

    coin_id : str
        coin_id of the coin in CoinGecko's API
    vs_currency : str
        The target currency of market data(usd, eur, jpy, etc.)
    days : str
        Data up to number of days ago(1 / 30 / max)"""

    ohcl = get_ohcl(coin_id, vs_currency, days)
    ohcl = convert_timestamp(ohcl)
    time.sleep(10)
    volume = get_volume(coin_id, vs_currency, days)
    volume = convert_timestamp(volume)
    time.sleep(10)
    merged = ohcl.join(volume.set_index('date_price'), on='date_price')
    # Reorder the columns
    merged = merged[['date_price', 'open', 'high', 'low', 'close', 'volume']]
    # Drop duplicated values in the date_price column
    merged.drop_duplicates(subset='date_price', keep='first', inplace=True)
    # Since the API returns an empty volume record for the last one, we drop it
    merged.drop(index=merged.index[-1], axis=0, inplace=True)
    #merged['coin_id'] = coin_id
    return merged


def get_latest_timestamp(db, table_name):

    """Returns the latest timestamp stored in the table's database"""

    metadata = MetaData()
    try:
        table = Table(table_name, metadata, schema="public", autoload_with=db)
        with db.connect() as connection:
            result = connection.execute(text(f"SELECT MAX(date_price) FROM {table_name}")).scalar()
        return result
    except NoSuchTableError:
        return None


def store_data_to_db(df, db, table_name):

    """Stores a DataFrame to a database

    Parameters:

    df : pandas.core.frame.DataFrame
        DataFrame to be stored
    db :
        SQLAlchemy's engine object
    days : str
        Data up to number of days ago(1 / 30 / max)
    """

    latest_timestamp = get_latest_timestamp(db, table_name)

    if latest_timestamp is not None:
        # Filter rows with timestamps greater than the latest timestamp in the table
        df = df[df['date_price'] > latest_timestamp]

    # Append data to the table (create table if not exists)
    df.to_sql(table_name, db, if_exists="append", index=False)


timeframes = {'half_hour': '1', 'four_hours': '30', 'four_days': 'max'}
ticker_vs_currency = ['ripple', 'usd']
data = {key: pull_coin_data(*ticker_vs_currency, values) for key, values in timeframes.items()}

db_name = 'data_acquisition'
db_user = 'acquisition'
db_pass = '0PZ9TVXV'
db_host = 'db'
db_port = '5432'

# Connect to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

for key, values in data.items():
    store_data_to_db(values, db, key)  # table_names[key]
    
print('Done')
