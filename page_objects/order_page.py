from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
from .base_page import BasePage

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def _close_cookies_banner(self):
        try:
            btn = self.find_element((By.CSS_SELECTOR, ".App_CookieButton__3cvqF"))
            self.driver.execute_script("arguments[0].click();", btn)
        except NoSuchElementException:
            pass

    def _select_metro(self, metro):
        for attempt in range(4):
            metro_input = self.wait_for_clickable((By.CSS_SELECTOR, '.select-search__input'))
            metro_input.click()
            metro_input.send_keys(Keys.CONTROL, 'a')
            metro_input.send_keys(Keys.DELETE)
            metro_input.send_keys(metro)

            option = None
            try:
                option = self.wait_for_visibility((By.CSS_SELECTOR, '.select-search__option'))
            except TimeoutException:
                metro_input.send_keys(Keys.ARROW_DOWN)
                try:
                    option = self.wait_for_visibility((By.CSS_SELECTOR, '.select-search__option'))
                except TimeoutException:
                    continue

            option.click()

            try:
                value = self.find_element((By.CSS_SELECTOR, '.select-search__input')).get_attribute('value')
            except NoSuchElementException:
                return True

            if value:
                return True
        return False
    
    def fill_order_form(self, first_name, last_name, address, metro, phone):
        self._close_cookies_banner()

        fields = [
            ((By.XPATH, '//input[@placeholder="* Имя"]'), first_name),
            ((By.XPATH, '//input[@placeholder="* Фамилия"]'), last_name),
            ((By.XPATH, '//input[contains(@placeholder, "Адрес")]'), address),
            ((By.XPATH, '//input[contains(@placeholder, "Телефон")]'), phone),
        ]
        for locator, value in fields:
            el = self.wait_for_clickable(locator)
            el.clear()
            el.send_keys(value)

        if not self._select_metro(metro):
            raise AssertionError(f"Не удалось выбрать станцию метро: {metro}")

        try:
            self.find_element((By.CSS_SELECTOR, '.select-search__input'))
        except NoSuchElementException:
            self.wait_for_presence((By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]'))
            return

        self.click((By.XPATH, '//button[text()="Далее"]'))
        self.wait_for_presence((By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]'))

    def fill_delivery_form(self):
        date_field = self.wait_for_clickable((By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]'))
        date_field.click()

        today = date.today()
        day_xpath = (
            '//div[contains(@class, "react-datepicker__day")'
            ' and not(contains(@class, "--outside-month"))'
            ' and not(contains(@class, "--disabled"))'
            f' and normalize-space(text())="{today.day}"]'
        )
        self.click((By.XPATH, day_xpath))

        self.click((By.CSS_SELECTOR, '.Dropdown-control'))
        self.click((By.CSS_SELECTOR, '.Dropdown-option'))

    def _modal_state(self, driver):
        if driver.find_elements(By.XPATH, '//button[text()="Да"]'):
            return "confirm"
        if driver.find_elements(
            By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]'
        ):
            return "success"
        return False

    def submit_order(self):
        try:
            self.find_element((By.CSS_SELECTOR, '.Dropdown-option'))
            self.find_element((By.TAG_NAME, 'body')).click()
        except NoSuchElementException:
            pass

        btn = self.wait_for_clickable((By.CSS_SELECTOR, 'button.Button_Middle__1CSJM:nth-child(2)'))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

        # Ожидаем изменения состояния модального окна
        WebDriverWait(self.driver, 10).until(self._modal_state)
        state = self._modal_state(self.driver)
        
        if state == "confirm":
            self.click((By.XPATH, '//button[text()="Да"]'))

        # Ожидаем появления сообщения об успехе
        self.wait_for_visibility((By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]'))
        print("Заказ успешно оформлен!")

    def check_success_message(self):
        element = self.wait_for_visibility((By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]'))
        return element.text