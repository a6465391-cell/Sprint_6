import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox import service as ff_service
from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage

test_data = [
    {"first_name": "Иван", "last_name": "Иванов", "address": "ул. Ленина, 1",
     "metro": "ВДНХ", "phone": "+79991112233", "button": "top"},
    {"first_name": "Мария", "last_name": "Петрова", "address": "пр. Мира, 5",
     "metro": "Охотный ряд", "phone": "+79994445566", "button": "bottom"},
]


@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий")
@pytest.mark.parametrize("data", test_data)
def test_order_flow(data):
    service = ff_service.Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()

    main_page = MainPage(driver)
    order_page = OrderPage(driver)

    try:
        driver.get("https://qa-scooter.praktikum-services.ru/")

        # --- ШАГ 1: Клик по кнопке "Заказать" (верхняя или нижняя) ---
        if data["button"] == "top":
            main_page.click_order_top()
        else:
            main_page.click_order_bottom()

        # --- ШАГ 2: Заполнение шага 1 (имя, фамилия, адрес, метро, телефон) ---
        order_page.fill_order_form(
            data["first_name"],
            data["last_name"],
            data["address"],
            data["metro"],
            data["phone"],
        )

        # --- ШАГ 3: Заполнение шага 2 (дата + срок аренды) ---
        order_page.fill_delivery_form()

        # --- ШАГ 4: «Заказать» + подтверждение в модалке ---
        order_page.submit_order()

        # --- ШАГ 5: Проверка успеха ---
        success_msg = order_page.check_success_message()
        assert "оформлен" in success_msg.lower(), f"Текст успеха не найден: {success_msg}"

    finally:
        driver.quit()

