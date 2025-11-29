#!/bin/bash
echo "Запуск WEB UI тестов OpenBMC..."

echo "Создание/обновление venv..."
rm -rf lab4/venv || true
cd lab4 || { echo "Директория lab4 не найдена"; exit 1; }
python3 -m venv venv
source venv/bin/activate || { echo "Ошибка активации venv"; exit 1; }
cd ..

pip install --upgrade pip
pip install pytest pytest-html pytest-selenium || { echo "Ошибка установки pytest"; exit 1; }
# Установка Chrome и Chromedriver для Selenium
echo "Установка Chrome для Selenium..."
sudo apt-get update
sudo apt-get install -y wget gnupg2 software-properties-common
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Chromedriver (автоматически под версию Chrome)
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*}/chromedriver_linux64.zip"
unzip /tmp/chromedriver.zip -d /tmp/
sudo mv /tmp/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

echo "Проверка тестов:"
ls -la lab4/openbmc_tests/*.py || { echo "Тестовые файлы не найдены"; exit 1; }

echo "Запуск pytest..."
cd lab4 || exit 1
pytest openbmc_tests/ \
    --html=test-report.html \
    --self-contained-html \
    -v \
    --tb=short \
    --junitxml=../reports/webui-tests.xml || { echo "Тесты провалились"; exit 1; }

echo "WEB UI тесты завершены!"
echo "Отчет: lab4/test-report.html"
ls -la test-report.html
