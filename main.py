from os import getenv
from dotenv import load_dotenv
from clickhouse import connection
from asyncio import sleep, run
from clickhouse_driver import Client
import checks

load_dotenv()

client = Client(host=getenv('CLICKHOUSE_HOST'),
                port=getenv('CLICKHOUSE_PORT'),
                user=getenv('CLICKHOUSE_USER'),
                password=getenv('CLICKHOUSE_PASSWORD'))


async def start_analysis(click_client):
    connection.insert_data_to_vpn(10000, click_client)
    last_connections = connection.select_data_from_vpn(click_client)
    hashed_connections = checks.hash_connections(last_connections)
    connection.insert_data_into_anomaly(hashed_connections, click_client)
    await sleep(10)
    print('looped')


if __name__ == '__main__':
    while True:
        run(start_analysis(client))
