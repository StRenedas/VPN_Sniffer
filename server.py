from datetime import datetime
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from db.connection import ClickhouseDB
from generators.fake_data_generator import FakeDataGenerator
from detectors.anomaly_detector import AnomalyDetector
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
ch = ClickhouseDB()
fake_data_generator = FakeDataGenerator()
anomaly_detector = AnomalyDetector()


@app.on_event('startup')
@repeat_every(seconds=60)
def check_anomalies():
    try:
        last_connections = ch.select_data_from_vpn()
        ch.update_timestamp(datetime.now())
        connections_dict = anomaly_detector.connections_to_dict(last_connections)
        anomalies = anomaly_detector.collect_anomalies(connections_dict)
        ch.insert_data_into_anomaly(anomalies)
    except Exception:
        return {'message': 'Something went wrong'}


@app.get("/")
def root():
    return {'message': 'Server up and running!'}


@app.get("/anomalies")
def fetch_anomalies():
    try:
        return ch.select_data_from_anomaly()
    except Exception:
        return {'message': 'Something went wrong'}


@app.get("/generate")
def generate_fakes():
    try:
        fake_rows = fake_data_generator.generate_fake_logins(10000)
        ch.insert_data_to_vpn(fake_rows)
        return {'message': 'Generated 10000 fake rows of vpn connections'}
    except Exception:
        return {'message': 'Something went wrong'}
