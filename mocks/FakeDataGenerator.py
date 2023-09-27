from random import randrange, choice, uniform
from datetime import date, time


class FakeDataGenerator:
    __fake_usernames = ['Varkentin_V', 'Sosedov_S', 'Ivanov_I', 'Petrov_P', 'Sidorov_V']

    @staticmethod
    def _generate_fake_ip() -> str:
        ip_segments = [str(randrange(1, 256)) for _ in range(4)]
        return '.'.join(ip_segments)

    @staticmethod
    def _generate_fake_coordinates() -> tuple[float, float]:
        return round(uniform(-90.0, 90.0), 6), round(uniform(-180.0, 180.0), 6)

    @staticmethod
    def _generate_fake_time() -> str:
        return time(randrange(0, 24), randrange(0, 60), randrange(0, 60)).strftime("%H:%M:%S")

    @staticmethod
    def _generate_fake_date() -> date:
        return date(year=randrange(1970, 2022), month=randrange(1, 13), day=randrange(1, 29))

    def generate_fake_logins(self, n: int, max_id: int) -> list:
        return [
            (max_id + n, choice(self.__fake_usernames), self._generate_fake_ip(), *self._generate_fake_coordinates(),
             self._generate_fake_time(),
             self._generate_fake_date()) for n in
            range(1, n + 1)]
