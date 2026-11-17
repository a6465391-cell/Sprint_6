import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox import service as ff_service
from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage

TEST_DATA_TOP = [
    {"first_name": "Иван", "last_name": "Иванов", "address": "ул. Ленина, 1",
     "metro": "ВДНХ", "phone": "+79991112233"},]
TEST_DATA_BOTTOM = [
    {"first_name": "Мария", "last_name": "Петрова", "address": "пр. Мира, 5",
     "metro": "Охотный ряд", "phone": "+79994445566"},]

@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий через верхнюю кнопку")
@pytest.mark.parametrize("data", TEST_DATA_TOP)
def test_order_flow_top_button(data):
    service = ff_service.Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()

    main_page = MainPage(driver)
    order_page = OrderPage(driver)

    try:
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        main_page.click_order_top()

        order_page.fill_order_form(
            data["first_name"],
            data["last_name"],
            data["address"],
            data["metro"],
            data["phone"],
        )
        order_page.fill_delivery_form()
        order_page.submit_order()
        
        success_msg = order_page.check_success_message()
        assert "оформлен" in success_msg.lower(), f"Текст успеха не найден: {success_msg}"

    finally:
        driver.quit()

@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий через нижнюю кнопку")
@pytest.mark.parametrize("data", TEST_DATA_BOTTOM)
def test_order_flow_bottom_button(data):
    service = ff_service.Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()

    main_page = MainPage(driver)
    order_page = OrderPage(driver)

    try:
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        main_page.click_order_bottom()

        order_page.fill_order_form(
            data["first_name"],
            data["last_name"],
            data["address"],
            data["metro"],
            data["phone"],
        )
        order_page.fill_delivery_form()
        order_page.submit_order()
        
        success_msg = order_page.check_success_message()
        assert "оформлен" in success_msg.lower(), f"Текст успеха не найден: {success_msg}"

    finally:
        driver.quit()

