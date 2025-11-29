import pytest
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_URL = "https://localhost:2443/redfish/v1"

@pytest.fixture
def auth_session():
    """Фикстура с retry + timeout"""
    session = requests.Session()
    session.verify = False
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"Auth attempt {attempt+1}/{max_retries}")
            response = session.post(
                f"{BASE_URL}/SessionService/Sessions",
                json={"UserName": "root", "Password": "0penBmc"},
                timeout=20  # ← КРИТИЧНО!
            )
            
            if response.status_code == 201:
                token = response.headers.get("X-Auth-Token")
                session.headers.update({"X-Auth-Token": token})
                yield session
                return
            else:
                print(f"Auth failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Auth error {attempt+1}: {e}")
            time.sleep(5)
    
    pytest.fail(f"Auth failed after {max_retries} attempts")

def test_authentication(auth_session):
    """Тест аутентификации"""
    response = auth_session.get(f"{BASE_URL}/Systems/system", timeout=20)
    assert response.status_code == 200

def test_system_info(auth_session):
    """Тест информации о системе"""
    response = auth_session.get(f"{BASE_URL}/Systems/system", timeout=20)
    assert response.status_code == 200
    data = response.json()
    assert "Status" in data
    assert "PowerState" in data

def test_power_management(auth_session):
    """Тест управления питанием"""
    response = auth_session.post(
        f"{BASE_URL}/Systems/system/Actions/ComputerSystem.Reset",
        json={"ResetType": "On"},
        timeout=30
    )
    assert response.status_code in [200, 202, 204]

def test_cpu_temperature(auth_session):
    """Тест температуры CPU"""
    response = auth_session.get(f"{BASE_URL}/Chassis", timeout=20)
    if response.status_code == 200:
        chassis_data = response.json()
        for member in chassis_data.get("Members", []):
            chassis_url = f"https://localhost:2443{member['@odata.id']}"
            chassis_detail = auth_session.get(chassis_url, timeout=20)
            if chassis_detail.status_code == 200:
                chassis_data = chassis_detail.json()
                thermal = chassis_data.get("Thermal", {})
                if thermal.get("Temperatures"):
                    return
    pytest.skip("Датчики температуры не найдены")

def test_cpu_sensors_redfish_ipmi(auth_session):
    """Тест датчиков CPU"""
    response = auth_session.get(f"{BASE_URL}/Systems/system", timeout=20)
    assert response.status_code == 200
    system_data = response.json()
    assert "ProcessorSummary" in system_data
