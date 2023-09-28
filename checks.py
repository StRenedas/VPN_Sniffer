import pprint
from math import cos, sin, acos
from uuid import uuid4

AVG_SPEED_PER_SECOND = 926 / 3600
EARTH_RADIUS = 6371


def calculate_distance(latitude_a: float, latitude_b: float, longitude_a: float, longitude_b: float) -> float:
    cos_d = sin(latitude_a) * sin(latitude_b) + cos(latitude_a) * cos(latitude_b) * cos(longitude_a - longitude_b)
    d = acos(cos_d)
    return d * EARTH_RADIUS


def is_anomaly(vpn_rows: list[tuple]) -> bool:
    if len(vpn_rows) < 2:
        return False

    datetime_1 = vpn_rows[0][3]

    datetime_2 = vpn_rows[1][3]

    delta = datetime_1 - datetime_2

    return calculate_distance(vpn_rows[0][1], vpn_rows[1][1], vpn_rows[0][2],
                              vpn_rows[1][2]) / AVG_SPEED_PER_SECOND > delta.total_seconds()


def connections_to_dict(connections) -> dict:
    connections_map = {}
    for data in connections:
        if data[1] not in connections_map:
            connections_map[data[1]] = [(data[0], *data[3:6])]
        else:
            connections_map[data[1]] += [(data[0], *data[3:6])]
    pprint.pprint(connections_map)
    return connections_map


def prep_anomalies(last_connections: dict) -> list:
    return [(uuid4(), values[0][0], user) for user, values in last_connections.items() if is_anomaly(values)]
