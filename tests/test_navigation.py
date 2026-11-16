import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from page_objects.main_page import MainPage

@allure.epic("Навигация")
@allure.feature("Проверка ссылок")
class TestNavigation:

    @allure.story("Переход на главную Самоката по клику на логотип")
    def test_click_scooter_logo_goes_to_main(self):
        service = Service(executable_path="geckodriver.exe")
        driver = webdriver.Firefox(service=service)
        
        try:
            page = MainPage(driver)
            driver.get("https://qa-scooter.praktikum-services.ru/")
            
            # Используем метод из MainPage
            page.click_scooter_logo()
            
            # Проверяем, что вернулись на главную (URL не изменился)
            assert driver.current_url == "https://qa-scooter.praktikum-services.ru/"
            assert "Самокат" in driver.title or "Scooter" in driver.title
            
        finally:
            driver.quit()

    @allure.story("Переход на Дзен по клику на логотип Яндекса (в новом окне)")
    def test_click_yandex_logo_opens_zen_in_new_tab(self):
        service = Service(executable_path="geckodriver.exe")
        driver = webdriver.Firefox(service=service)
        
        try:
            page = MainPage(driver)
            driver.get("https://qa-scooter.praktikum-services.ru/")
            
            # Запоминаем текущую вкладку
            main_window = driver.current_window_handle
            
            # Используем метод из MainPage
            page.click_yandex_logo()
            
            # Ждем появления новой вкладки
            # Можно добавить простой цикл ожидания, если WebDriverWait не импортирован в тесте
            import time
            start_time = time.time()
            while len(driver.window_handles) <= 1:
                if time.time() - start_time > 15:
                    raise TimeoutError("Новая вкладка не появилась за 15 секунд")
                time.sleep(0.5)
            
            # Переключаемся на новую вкладку
            driver.switch_to.window(driver.window_handles[-1])
            
            # Ждем загрузки Дзена
            import time
            start_time = time.time()
            while "dzen.ru" not in driver.current_url:
                if time.time() - start_time > 15:
                    raise TimeoutError("Дзен не загрузился за 15 секунд")
                time.sleep(0.5)
            
            assert "Дзен" in driver.title or "dzen" in driver.current_url
            
        finally:
            driver.quit()
