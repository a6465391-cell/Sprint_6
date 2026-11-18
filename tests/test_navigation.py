import pytest
import allure
from page_objects.main_page import MainPage

BASE_URL = "https://qa-scooter.praktikum-services.ru/"

@allure.epic("Навигация")
@allure.feature("Проверка ссылок")
class TestNavigation:

    @allure.story("Переход на главную Самоката по клику на логотип")
    def test_click_scooter_logo_goes_to_main(self, driver):
        page = MainPage(driver)
        driver.get(BASE_URL)
        
        page.click_scooter_logo()
        
        assert driver.current_url == BASE_URL, f"Ожидался URL {BASE_URL}, но получен {driver.current_url}"

    @allure.story("Переход на Дзен по клику на логотип Яндекса")
    def test_click_yandex_logo_opens_zen_in_new_tab(self, driver):
        page = MainPage(driver)
        driver.get(BASE_URL)
        
        page.click_yandex_logo()
        
        page.switch_to_new_tab()
        
        current_url = page.get_current_url()
        
        assert "dzen.ru" in current_url, f"Ожидался переход на dzen.ru, но получен {current_url}"