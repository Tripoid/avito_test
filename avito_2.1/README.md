# Тесты API Avito

Этот проект содержит автоматизированные тесты для API Avito. Тесты написаны на Python с использованием pytest.

## Структура проекта

`test_api.py` - основной файл с тестами
`conftest.py` - конфигурация pytest
`requirements.txt` - зависимости

## Установка зависимостей
`pip install -r requirements.txt`

## Запуск тестов

### Запуск всех тестов
`pytest test_api.py`

### Запуск с подробным выводом
`pytest test_api.py -v`

### Запуск без вывода трассировки
`pytest test_api.py --tb=no`