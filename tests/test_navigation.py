import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from page_objects.main_page import MainPage

@allure.epic("Навигация")
@allure.feature("Проверка ссылок")
class TestNavigation:

    @allure.story("Переход на главную Самоката по клику на логотип")
    def test_click_scooter_logo_goes_to_main(self, driver):
        # driver уже создан и maximizing выполнен в фикстуре
        wait = WebDriverWait(driver, 10)
        page = MainPage(driver)
        
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        page.click_scooter_logo()
        
        wait.until(lambda d: "scooter" in d.current_url or "Самокат" in d.title)
        
        assert "Самокат" in driver.title or "Scooter" in driver.title.lower()

    @allure.story("Переход на Дзен по клику на логотип Яндекса (в новом окне)")
    def test_click_yandex_logo_opens_zen_in_new_tab(self, driver):
        wait = WebDriverWait(driver, 15)
        page = MainPage(driver)
        
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        main_window = driver.current_window_handle
        
        page.click_yandex_logo()
        
        wait.until(lambda d: len(d.window_handles) > 1)
        
        driver.switch_to.window(driver.window_handles[-1])
        
        wait.until(lambda d: "dzen.ru" in d.current_url)
        
        assert "dzen.ru" in driver.current_url
        
        driver.switch_to.window(main_window)
