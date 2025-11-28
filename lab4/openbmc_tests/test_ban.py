from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    for i in range(3):
        driver.get("https://localhost:2443")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        driver.find_element(By.ID, "username").send_keys("root")
        driver.find_element(By.ID, "password").send_keys("wrong")
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if "Log in" in btn.text:
                btn.click()
                break
        
        time.sleep(5)
        print(f"Попытка {i+1}/3")
    
    print("Блокировка аккаунта")
    
except Exception as e:
    print(f"Ошибка: {e}")
    
finally:
    driver.quit()