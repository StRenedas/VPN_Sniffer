from clickhouse_driver import Client
from mocks import FakeDataGenerator
import checks

fake_generator = FakeDataGenerator.FakeDataGenerator()


def insert_data_to_vpn(number_of_fake_rows: int, click_client: Client):
    max_id = click_client.execute('SELECT MAX(id) FROM VPN')[0][0] + 1 or 0
    fake_data = fake_generator.generate_fake_logins(n=number_of_fake_rows, max_id=max_id)
    click_client.execute('INSERT INTO VPN (*) VALUES', fake_data)
    click_client.disconnect_connection()


def select_data_from_vpn(click_client: Client):
    result = click_client.execute(
        "SELECT * FROM VPN GROUP BY username, id, IP, latitude, longitude, time, date ORDER BY username, date DESC LIMIT 2 BY username")
    click_client.disconnect_connection()
    return result


def insert_data_into_anomaly(last_connections: dict, click_client: Client):
    max_id = click_client.execute('SELECT MAX(id) FROM ANOMALY')[0][0] + 1 or 0
    anomalies = checks.prep_anomalies(last_connections, max_id=max_id)
    click_client.execute("INSERT INTO ANOMALY (*) VALUES ", anomalies)
    click_client.disconnect_connection()
