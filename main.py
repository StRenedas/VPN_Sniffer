import datetime
import pprint
from dotenv import load_dotenv
from db.connection import ClickhouseDB
from generators.FakeDataGenerator import FakeDataGenerator
from AnomalyDetector import AnomalyDetector
from asyncio import sleep, run

load_dotenv()

DB_connection = ClickhouseDB()
fake_data_generator = FakeDataGenerator()
anomaly_detector = AnomalyDetector()


async def start_analysis():
    min_time = datetime.datetime.min
    while True:
        try:
            fake_rows = fake_data_generator.generate_fake_logins(10)
            DB_connection.insert_data_to_vpn(fake_rows)
            await sleep(10)

            fake_rows = fake_data_generator.generate_fake_logins(10)
            DB_connection.insert_data_to_vpn(fake_rows)
            await sleep(5)

            last_connections = DB_connection.select_data_from_vpn(min_time)
            min_time = datetime.datetime.now()

            connections_dict = anomaly_detector.connections_to_dict(last_connections)
            anomalies = anomaly_detector.collect_anomalies(connections_dict)
            DB_connection.insert_data_into_anomaly(anomalies)

            print('Anomalies found:')
            pprint.pprint(anomalies)
            await sleep(60)

        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    run(start_analysis())
