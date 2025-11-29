#!/bin/bash
set -e

echo "Очистка старого контейнера qemu-openbmc..."
docker rm -f qemu-openbmc 2>/dev/null || true
echo "OK"

echo "Сборка qemu-openbmc образа..."
docker build -t qemu-openbmc ./docker/qemu

echo "Запуск OpenBMC QEMU..."
docker run -d --name qemu-openbmc \
  -p 2222:2222 -p 2443:443 -p 2623:623 \
  qemu-openbmc

echo "OpenBMC запущен. Ждем готовности..."
sleep 30  
