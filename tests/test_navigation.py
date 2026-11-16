import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("Навигация")
@allure.feature("Проверка ссылок")
class TestNavigation:

    @allure.story("Переход на главную Самоката по клику на логотип")
    def test_click_scooter_logo_goes_to_main(self):
        service = Service(executable_path="geckodriver.exe")
        driver = webdriver.Firefox(service=service)
        wait = WebDriverWait(driver, 15)  # Увеличили таймаут до 15 сек
        
        try:
            driver.get("https://qa-scooter.praktikum-services.ru/")
            
            # 1. Находим логотип Самоката
            logo_scooter = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Header_LogoScooter__3lsAR")))
            
            # 2. Кликаем
            logo_scooter.click()
            
            # 3. ЖДЕМ, пока URL станет правильным (это надежнее, чем ждать title)
            # Ждем, пока текущий URL будет равен главной странице
            wait.until(lambda d: d.current_url == "https://qa-scooter.praktikum-services.ru/")
            
            # 4. Теперь безопасно проверяем заголовок
            assert "Самокат" in driver.title or "Scooter" in driver.title
            
        finally:
            driver.quit()

    @allure.story("Переход на Дзен по клику на логотип Яндекса (в новом окне)")
    def test_click_yandex_logo_opens_zen_in_new_tab(self):
        service = Service(executable_path="geckodriver.exe")
        driver = webdriver.Firefox(service=service)
        wait = WebDriverWait(driver, 15)
        
        try:
            driver.get("https://qa-scooter.praktikum-services.ru/")
            
            # 1. Находим логотип Яндекса
            logo_yandex = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Header_LogoYandex__3TSOI")))
            
            # 2. Запоминаем текущую вкладку
            main_window = driver.current_window_handle
            
            # 3. Кликаем
            logo_yandex.click()
            
            # 4. Ждем появления новой вкладки
            wait.until(lambda d: len(d.window_handles) > 1)
            
            # 5. Переключаемся на новую вкладку (последнюю в списке)
            driver.switch_to.window(driver.window_handles[-1])
            
            # 6. Ждем загрузки Дзена (проверяем URL)
            wait.until(lambda d: "dzen.ru" in d.current_url)
            
            # 7. Проверка заголовка
            assert "Дзен" in driver.title or "dzen" in driver.current_url
            
        finally:
            driver.quit()
