#!/bin/bash
set -e

echo "=== НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ OpenBMC ==="
echo "⏳ Проверка OpenBMC..."

pip3 install locust || echo "Locust уже установлен"

echo "Locust: 20 users, 5/sec, 60 сек → https://localhost:2443"
cd lab6
locust -f locustfile.py \
       --headless \
       --host=https://localhost:2443 \
       -u 20 -r 5 \
       --run-time 60s \
       --html=locust-report.html \
       --csv=locust-report

echo "НАГРУЗКА ЗАВЕРШЕНА!"
echo "Отчёт: lab6/locust-report.html"
ls -la locust-report.*

echo "📈 СТАТИСТИКА:"
grep -E "requests|failure|median|99%" locust-report.html || true
