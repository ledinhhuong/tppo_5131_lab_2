# tppo_5131 ЛР №2

### Установка зависимостей
В окне терминала: `pip install -r requirements.txt`
### Сервер
В окне терминала:
- Запустить сервера, `python tppo_server_5131.py ip port`. Где ip - адрес; port - порт

Пример: `python tppo_server_5131.py 127.0.0.1 5000`
### Клиенты
В других окнах терминала:
- Запустить клиенты, `python tppo_client_5131.py ip port`. Где ip - адрес; port - порт
- Установить проценты сдвига полотна пропуска светового потока, `set shaer X` и `set flux X`. Где X = 0 .. 100
- Получить значения процентов сдвига полотна, пропуска светового потока и текущей освещенности с внешней стороны, `get shaer`, `get flux` и `get illumination`

Пример: `python tppo_client_5131.py 127.0.0.1 5000`; `set shaer 52`; `get flux`

Установить данных вручную в файле устройства `blinds.txt`
### Проверка REST APIs 
В браузере открыть следующие ссылки:
- Получить значения процентов сдвига полотна, пропуска светового потока и текущей освещенности с внешней стороны, `http://<ip>:<port>/blinds/<parameter>`. Где ip - адрес; port - порт; parameter - shaer, flux или illumination
- Установить проценты сдвига полотна пропуска светового потока, `http://<ip>:<port>/blinds?<parameter>=<X>`.Где ip - адрес; port - порт; parameter - shaer или flux, X = 0 .. 100

Пример: `http://127.0.0.1:5000/blinds/illumination`; `http://127.0.0.1:5000/blinds?flux=59`
