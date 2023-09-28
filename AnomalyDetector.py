from math import cos, sin, acos
from uuid import uuid4


class AnomalyDetector:
    AVG_SPEED_PER_SECOND = 926 / 3600
    EARTH_RADIUS = 6371

    def __calculate_distance(self, latitude_a: float, latitude_b: float, longitude_a: float,
                             longitude_b: float) -> float:
        cos_d = sin(latitude_a) * sin(latitude_b) + cos(latitude_a) * cos(latitude_b) * cos(longitude_a - longitude_b)
        d = acos(cos_d)
        return d * self.EARTH_RADIUS

    def __is_anomaly(self, vpn_rows: list[tuple]) -> bool:
        if len(vpn_rows) < 2:
            return False

        datetime_1 = vpn_rows[0][3]
        datetime_2 = vpn_rows[1][3]
        delta = datetime_1 - datetime_2

        return self.__calculate_distance(vpn_rows[0][1], vpn_rows[1][1], vpn_rows[0][2],
                                         vpn_rows[1][2]) / self.AVG_SPEED_PER_SECOND > delta.total_seconds()

    def collect_anomalies(self, last_connections: dict) -> list:
        return [(uuid4(), values[0][0], user) for user, values in last_connections.items() if self.__is_anomaly(values)]

    @staticmethod
    def connections_to_dict(connections: list) -> dict:
        connections_map = {}
        for data in connections:
            if data[1] not in connections_map:
                connections_map[data[1]] = [(data[0], *data[3:6])]
            else:
                connections_map[data[1]] += [(data[0], *data[3:6])]
        return connections_map
