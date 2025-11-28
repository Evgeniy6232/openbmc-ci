from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
try:
    # Логинимся
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
    
    print("=== ПОИСК ЭЛЕМЕНТОВ УПРАВЛЕНИЯ ===")
    
    # Ищем все кнопки
    print("\n📋 Все кнопки на странице:")
    all_buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, btn in enumerate(all_buttons):
        print(f"{i+1}. Текст: '{btn.text}', ID: '{btn.get_attribute('id')}', Class: '{btn.get_attribute('class')}'")
    
    # Ищем все ссылки
    print("\n🔗 Все ссылки на странице:")
    all_links = driver.find_elements(By.TAG_NAME, "a")
    for i, link in enumerate(all_links):
        if link.text:  # Только с текстом
            print(f"{i+1}. Текст: '{link.text}', Href: '{link.get_attribute('href')}'")
    
    # Ищем все элементы с текстом Power, Server, Host
    print("\n⚡️ Элементы с Power/Server/Host:")
    power_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'POWER', 'power'), 'power') or contains(translate(text(), 'SERVER', 'server'), 'server') or contains(translate(text(), 'HOST', 'host'), 'host')]")
    for i, elem in enumerate(power_elements):
        if elem.text.strip():
            print(f"{i+1}. Текст: '{elem.text}', Тег: {elem.tag_name}")
    
    print("\n⏳ Браузер открыт 60 секунд для ручного осмотра...")
    time.sleep(60)
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    time.sleep(60)
finally:
    driver.quit()