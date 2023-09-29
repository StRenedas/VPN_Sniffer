from os import getenv
from clickhouse_driver import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class ClickhouseDB:

    def __init__(self):
        self.client = Client(host=getenv('CLICKHOUSE_HOST'),
                             port=getenv('CLICKHOUSE_PORT'),
                             user=getenv('CLICKHOUSE_ADMIN_USER'),
                             password=getenv('CLICKHOUSE_ADMIN_PASSWORD'))
        self.__timestamp = datetime.min

    def insert_data_to_vpn(self, fake_rows):
        try:
            self.client.execute('INSERT INTO VPN (*) VALUES', fake_rows)
        except Exception as ex:
            print(ex)

    def select_data_from_vpn(self):
        try:
            return self.client.execute(
                "SELECT * FROM VPN WHERE %(min_time)s < datetime AND datetime < now() GROUP BY username, id, IP, latitude, longitude, datetime ORDER BY username, datetime DESC LIMIT 2 BY username",
                {'min_time': self.__timestamp})
        except Exception as ex:
            print(ex)

    def insert_data_into_anomaly(self, anomalies: list):
        try:
            self.client.execute("INSERT INTO ANOMALY (*) VALUES ", anomalies)
        except Exception as ex:
            print(ex)

    def select_data_from_anomaly(self):
        try:
            return self.client.execute("SELECT * FROM ANOMALY")
        except Exception as ex:
            print(ex)

    def update_timestamp(self, new_timestamp):
        self.__timestamp = new_timestamp
