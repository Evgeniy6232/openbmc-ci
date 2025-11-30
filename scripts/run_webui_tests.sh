#!/bin/bash
echo "Запуск WEB UI тестов OpenBMC..."

echo "Создание/обновление venv..."
rm -rf lab4/venv || true
cd lab4 || { echo "Директория lab4 не найдена"; exit 1; }
python3 -m venv venv
source venv/bin/activate || { echo "Ошибка активации venv"; exit 1; }
cd ..

pip install --upgrade pip
pip install pytest pytest-html pytest-selenium webdriver-manager || { echo "Ошибка установки pytest"; exit 1; }

echo "Chromedriver будет установлен автоматически через webdriver-manager"

echo "Проверка тестов:"
ls -la lab4/openbmc_tests/*.py || { echo "Тестовые файлы не найдены"; exit 1; }

echo "
Запуск pytest..."
cd lab4 || exit 1
pytest openbmc_tests/ \
    --html=test-report.html \
    --self-contained-html \
    -v \
    --tb=short \
    --junitxml=../reports/webui-tests.xml || { echo "Тесты провалились"; exit 1; }

echo "WEB UI тесты завершены!"
echo "Отчеты:"
echo "  - lab4/test-report.html"
echo "  - reports/webui-tests.xml"
ls -la ../lab4/test-report.html ../reports/webui-tests.xml || echo "Некоторые отчеты не созданы"
