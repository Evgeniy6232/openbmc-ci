#!/bin/bash
echo "🧪 Запуск автотестов lab5.py (Redfish API)..."

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

echo "⏳ Ждём готовности OpenBMC Redfish API (5 мин max)..."
SUCCESS=0
for i in {1..48}; do
    if curl -k -f -m 10 https://localhost:2443/redfish/v1/Systems >/dev/null 2>&1; then
        echo "OpenBMC Redfish API готов!"
        SUCCESS=1
        break
    fi
    echo "⏳ OpenBMC не готов ($i/30)... ждём 10s"
    sleep 10
done

if [ $SUCCESS -eq 0 ]; then
    echo "OpenBMC не запустился за 5 минут!"
    curl -k -v https://localhost:2443/redfish/v1/Systems || echo "Port 2443 недоступен"
    exit 1
fi

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
echo "Отчет: lab4/test-report.html"
ls -la test-report.html
