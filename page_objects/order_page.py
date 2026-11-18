import allure
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import date
from .base_page import BasePage

class OrderPage(BasePage):
    LOCATOR_ORDER_BTN = (By.XPATH, '(//button[contains(normalize-space(), "Заказать")])[last()]')
    
    LOCATOR_COOKIE_BTN = (By.CSS_SELECTOR, ".App_CookieButton__3cvqF")
    LOCATOR_METRO_INPUT = (By.CSS_SELECTOR, ".select-search__input")
    LOCATOR_METRO_OPTION = (By.CSS_SELECTOR, ".select-search__option")
    
    LOCATOR_FIELD_NAME = (By.XPATH, '//input[@placeholder="* Имя"]')
    LOCATOR_FIELD_LAST_NAME = (By.XPATH, '//input[@placeholder="* Фамилия"]')
    LOCATOR_FIELD_ADDRESS = (By.XPATH, '//input[contains(@placeholder, "Адрес")]')
    LOCATOR_FIELD_PHONE = (By.XPATH, '//input[contains(@placeholder, "Телефон")]')
    
    LOCATOR_NEXT_BTN = (By.XPATH, '//button[contains(text(), "Далее")]')
    LOCATOR_DATE_FIELD = (By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]')
    
    LOCATOR_DROPDOWN_CONTROL = (By.CSS_SELECTOR, ".Dropdown-control")
    LOCATOR_DROPDOWN_OPTION = (By.CSS_SELECTOR, ".Dropdown-option")
    
    LOCATOR_CONFIRM_BTN = (By.XPATH, '//button[contains(text(), "Да")]')
    LOCATOR_SUCCESS_MODAL = (By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]')

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Закрытие баннера с куки")
    def _close_cookies_banner(self):
        try:
            btn = self.find_element(self.LOCATOR_COOKIE_BTN)

            self.click_by_js(btn)
        except NoSuchElementException:
            pass

    @allure.step("Выбор станции метро: {metro}")
    def _select_metro(self, metro):
        for attempt in range(4):
            metro_input = self.wait_for_clickable(self.LOCATOR_METRO_INPUT)
            metro_input.click()
            metro_input.send_keys(Keys.CONTROL, 'a')
            metro_input.send_keys(Keys.DELETE)
            metro_input.send_keys(metro)

            option = None
            try:
                option = self.wait_for_visibility(self.LOCATOR_METRO_OPTION)
            except TimeoutException:
                metro_input.send_keys(Keys.ARROW_DOWN)
                try:
                    option = self.wait_for_visibility(self.LOCATOR_METRO_OPTION)
                except TimeoutException:
                    continue

            if option:
                # Клик через JS надежнее для выпадающих списков
                self.click_by_js(option)

            try:
                value = self.find_element(self.LOCATOR_METRO_INPUT).get_attribute('value')
            except NoSuchElementException:
                return True

            if value:
                return True
        return False
    
    @allure.step("Заполнение формы заказа (шаг 1): имя={first_name}, фамилия={last_name}, адрес={address}, метро={metro}, телефон={phone}")
    def fill_order_form(self, first_name, last_name, address, metro, phone):
        self._close_cookies_banner()

        fields = [
            (self.LOCATOR_FIELD_NAME, first_name),
            (self.LOCATOR_FIELD_LAST_NAME, last_name),
            (self.LOCATOR_FIELD_ADDRESS, address),
            (self.LOCATOR_FIELD_PHONE, phone), ]
        
        for locator, value in fields:
            el = self.wait_for_clickable(locator)
            el.clear()
            el.send_keys(value)

        if not self._select_metro(metro):
            raise AssertionError(f"Не удалось выбрать станцию метро: {metro}")

        try:
            self.find_element(self.LOCATOR_METRO_INPUT)
        except NoSuchElementException:
            self.wait_for_presence(self.LOCATOR_DATE_FIELD)
            return

        self.click(self.LOCATOR_NEXT_BTN)
        self.wait_for_presence(self.LOCATOR_DATE_FIELD)

    @allure.step("Заполнение формы доставки (шаг 2): выбор даты и срока аренды")
    def fill_delivery_form(self):
        date_field = self.wait_for_clickable(self.LOCATOR_DATE_FIELD)
        date_field.click()

        today = date.today()
        day_xpath = (
            '//div[contains(@class, "react-datepicker__day")'
            ' and not(contains(@class, "--outside-month"))'
            ' and not(contains(@class, "--disabled"))'
            f' and normalize-space(text())="{today.day}"]')
        self.click((By.XPATH, day_xpath))

        self.click(self.LOCATOR_DROPDOWN_CONTROL)
        self.click(self.LOCATOR_DROPDOWN_OPTION)

    @allure.step("Отправка заказа с подтверждением")
    def submit_order(self):

        btn = self.wait_for_clickable(self.LOCATOR_ORDER_BTN)
        self.scroll_to_element(btn)
        self.click_by_js(btn)  

        try:
            confirm_btn = self.wait_for_clickable(self.LOCATOR_CONFIRM_BTN)
            confirm_btn.click()
        except TimeoutException:
            pass

        self.wait_for_visibility(self.LOCATOR_SUCCESS_MODAL) 

    @allure.step("Проверка сообщения об успехе")
    def check_success_message(self):
        element = self.wait_for_visibility(self.LOCATOR_SUCCESS_MODAL)
        return element.text