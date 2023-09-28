# VPN_Sniffer

Сервис предназначен для анализа лога подключений пользователей  
и детектирования аномалий, связанных с возможным использованием VPN-соединения.

## Используемые технологии и библиотеки

- Python 3.10
- ClickHouse 23
- Docker
- Docker Compose
- clickhouse-driver 0.2.6
- python-dotenv 1.0.0

## Запуск сервиса

Для сборки и запуска контейнеров сервиса использовать команду

```bash
docker-compose -d
```

Логи работы сервиса выведены в stdout и доступны с использованием команды

```bash
docker logs
```

Для внешнего подключения к БД использовать адрес ```localhost:8123```  
и имя пользователя/пароль из файла .env.docker