from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_logs_check():
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
        
        for btn in driver.find_elements(By.TAG_NAME, "button"):
            if "Log in" in btn.text:
                btn.click()
                break
        
        time.sleep(3)
        
        for link in driver.find_elements(By.TAG_NAME, "a"):
            if "Health" in link.text or "Event" in link.text:
                driver.execute_script("arguments[0].click();", link)
                break
        
        time.sleep(3)
        
        if "log" in driver.current_url.lower() or "event" in driver.current_url.lower():
            print("Проверка пошла успешно")
        else:
            print("Не удалось перейти на страницу логов")
        
        time.sleep(30)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        driver.quit()

test_logs_check()