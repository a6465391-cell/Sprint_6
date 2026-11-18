import pytest
import allure
from page_objects.main_page import MainPage
from page_objects.order_page import OrderPage

BASE_URL = "https://qa-scooter.praktikum-services.ru/"

@allure.epic("Заказ самоката")
@allure.feature("Позитивный сценарий")
class TestOrderFlow:

    @allure.story("Оформление заказа через верхнюю кнопку «Заказать»")
    def test_order_flow_top_button(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        driver.get(BASE_URL)
        
        main_page.click_order_top()
        
        order_page.fill_order_form(
            first_name="Иван",
            last_name="Иванов",
            address="ул. Ленина, 1",
            metro="ВДНХ",
            phone="+79991112233"
        )
        
        order_page.fill_delivery_form()
        order_page.submit_order()
        
        success_msg = order_page.check_success_message()
        assert "оформлен" in success_msg.lower()

    @allure.story("Оформление заказа через нижнюю кнопку «Заказать»")
    def test_order_flow_bottom_button(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        driver.get(BASE_URL)
        
        main_page.click_order_bottom()
        
        order_page.fill_order_form(
            first_name="Мария",
            last_name="Петрова",
            address="пр. Мира, 5",
            metro="Охотный ряд",
            phone="+79994445566"
        )
        
        order_page.fill_delivery_form()
        order_page.submit_order()
        
        success_msg = order_page.check_success_message()
        assert "оформлен" in success_msg.lower()