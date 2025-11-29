#!/bin/bash
set -e

echo "=== НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ OpenBMC ==="
cd lab6

python3 -m venv locust-venv
source locust-venv/bin/activate
pip install locust requests[security] 

echo "Locust: 20 users, 5/sec, 60 сек → https://localhost:2443"

locust -f locustfile.py \
       --headless \
       --host=https://localhost:2443 \
       -u 20 -r 5 \
       --run-time 60s \
       --html=locust-report.html \
       --csv=locust-report

deactivate 

echo "НАГРУЗКА ЗАВЕРШЕНА!"
echo "Отчёт: lab6/locust-report.html"
ls -la locust-report.*

echo "СТАТИСТИКА:"
grep -E "requests|failure|median|99%" locust-report.html || true