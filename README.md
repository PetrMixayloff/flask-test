Тестовое приложение на фласк для парсинга сайтов с использование очереди задач redis queue.

Установка redis: `sudo apt-get install redis-server`

Откройте этот файл настроек в текстовом редакторе: 

`sudo nano /etc/redis/redis.conf`

Внутри файла найдите директиву `supervised`. По умолчанию установлено значение `no`, измените значение на `systemd`.

Запуск приложения `python3 app.py`

Запуск воркера редис `python3 worker.py`

Документация в swagger ui http://0.0.0.0:8888/
