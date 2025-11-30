#!/bin/bash
echo "Запуск автотестов lab5.py (Redfish API)..."

echo "Создание/обновление venv (только pytest + requests)..."
rm -rf lab4/venv_autotests || true
cd lab4 || { echo "Директория lab4 не найдена"; exit 1; }
python3 -m venv venv_autotests
source venv_autotests/bin/activate || { echo "Ошибка активации venv"; exit 1; }
cd ..


pip install --upgrade pip
pip install pytest pytest-html requests || { echo "Ошибка установки пакетов"; exit 1; }

echo "Проверка автотестов:"
ls -la lab4/openbmc_tests/lab5.py || { echo "Файл lab4/openbmc_tests/lab5.py не найден"; exit 1; }

echo "Запуск pytest..."
cd lab4 || exit 1
source venv_autotests/bin/activate
pytest openbmc_tests/lab5.py \
    --html=test-report.html \
    --self-contained-html \
    -v \
    --tb=short \
    --junitxml=../reports/autotests.xml || { echo "Автотесты провалились"; exit 1; }

echo "Автотесты завершены!"
echo "Отчеты:"
echo "  - lab4/test-report.html" 
echo "  - reports/autotests.xml"
ls -la ../lab4/test-report.html ../reports/autotests.xml || echo "Некоторые отчеты не созданы"
