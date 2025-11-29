#!/bin/bash

echo "🧪 Запуск WEB UI тестов OpenBMC..."

if [ ! -d "lab4/venv" ]; then
    echo "venv не найдена! Создаем..."
    cd lab4 || { echo "Директория lab4 не найдена"; exit 1; }
    python3 -m venv venv
    cd ..
fi

source lab4/venv/bin/activate || { echo "Ошибка активации venv"; exit 1; }

pip install --upgrade pip
pip install pytest pytest-html || { echo "Ошибка установки pytest"; exit 1; }

echo "Проверка тестов:"
ls -la lab4/openbmc_tests/*.py || { echo "Тестовые файлы не найдены"; exit 1; }

echo "🚀 Запуск pytest..."
cd lab4 || exit 1
pytest openbmc_tests/ \
    --html=test-report.html \
    --self-contained-html \
    -v \
    --tb=short || { echo "Тесты провалились"; exit 1; }

echo "WEB UI тесты завершены!"
echo "Отчет: lab4/test-report.html"
ls -la test-report.html
