from math import cos, sin, acos
from datetime import datetime

AVG_SPEED_PER_SECOND = 926 / 3600
EARTH_RADIUS = 6371


def calculate_distance(latitude_a: float, latitude_b: float, longitude_a: float, longitude_b: float) -> float:
    cos_d = sin(latitude_a) * sin(latitude_b) + cos(latitude_a) * cos(latitude_b) * cos(longitude_a - longitude_b)
    d = acos(cos_d)
    return d * EARTH_RADIUS


def is_anomaly(vpn_rows: list[tuple]) -> bool:
    time_1 = datetime.strptime(vpn_rows[0][3], "%H:%M:%S").time()
    datetime_1 = datetime.combine(vpn_rows[0][4], time_1)

    time_2 = datetime.strptime(vpn_rows[1][3], "%H:%M:%S").time()
    datetime_2 = datetime.combine(vpn_rows[1][4], time_2)
    delta = datetime_1 - datetime_2

    return calculate_distance(vpn_rows[0][1], vpn_rows[1][1], vpn_rows[0][2],
                              vpn_rows[1][2]) / AVG_SPEED_PER_SECOND > delta.total_seconds()


def hash_connections(connections) -> dict:
    new_dict = {}
    for data in connections:
        if data[1] not in new_dict:
            new_dict[data[1]] = [(data[0], *data[3:7])]
        else:
            new_dict[data[1]] += [(data[0], *data[3:7])]
    return new_dict


def prep_anomalies(last_connections: dict, max_id: int) -> list:
    anomalies = []
    for user in last_connections:
        anomaly_found = is_anomaly(last_connections[user])
        if anomaly_found:
            anomalies.append((max_id, last_connections[user][0][0], user))
            max_id += 1
    return anomalies
