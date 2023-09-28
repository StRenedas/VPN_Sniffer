from random import randrange, choice, uniform
from datetime import datetime
from uuid import uuid4


class FakeDataGenerator:
    __fake_usernames = ['Varkentin_V', 'Sosedov_S', 'Ivanov_I', 'Petrov_P', 'Sidorov_V', 'Andreev_A', 'Glebov_G']

    @staticmethod
    def _generate_fake_ip() -> str:
        ip_segments = [str(randrange(1, 256)) for _ in range(4)]
        return '.'.join(ip_segments)

    @staticmethod
    def _generate_fake_coordinates() -> tuple[float, float]:
        return round(uniform(-90.0, 90.0), 6), round(uniform(-180.0, 180.0), 6)

    def generate_fake_logins(self, number_of_fake_logins: int) -> list:
        return [
            (uuid4(),
             choice(self.__fake_usernames),
             self._generate_fake_ip(),
             *self._generate_fake_coordinates(),
             datetime.now()
             ) for _ in range(number_of_fake_logins)]
