from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_login(){
    service = Service(ChromeDriverManager().install())  
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)  

    try:
        driver.get("https://localhost:2443")
    
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
    
        username_field.send_keys("root")
    
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("0penBmc")
    
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if "Log in" in btn.text:
                btn.click()
                break
    
        print("Авторизация прошла успешно")
        time.sleep(20)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(20)
    
    finally:
        driver.quit()
}

test_login()