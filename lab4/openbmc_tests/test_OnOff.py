from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_power_control():
    service = Service(ChromeDriverManager().install())  
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)  
    try:
        
        driver.get("https://localhost:2443")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys("root")
        driver.find_element(By.ID, "password").send_keys("0penBmc")
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if "Log in" in btn.text:
                btn.click()
                break
        
        time.sleep(3)
        
        power_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#/operations/server-power-operations']"))
        )
        power_link.click()
        
        time.sleep(3)
        
        power_on_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Power on')]"))
        )
        print(f"Нашли кнопку: '{power_on_button.text}'")
        power_on_button.click()
        print("✅ Нажали кнопку Power on!")
        
        time.sleep(8)
        
        print("Тест прошел")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.quit()

test_power_control()