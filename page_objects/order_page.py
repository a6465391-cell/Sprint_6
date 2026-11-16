import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date

class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ---------- Вспомогательные ----------

    def _close_cookies_banner(self):
        """Закрывает баннер с куки, если он есть."""
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, ".App_CookieButton__3cvqF")
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
        except NoSuchElementException:
            pass

    def _select_metro(self, metro):
        """Выбирает станцию метро через выпадающий список. Повторяет до 4 попыток."""
        for attempt in range(4):
            metro_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select-search__input')))
            metro_input.click()  
            time.sleep(0.3)
            metro_input.send_keys(Keys.CONTROL, 'a')
            metro_input.send_keys(Keys.DELETE)
            metro_input.send_keys(metro)  
            time.sleep(0.5)

            option = None
            try:
                option = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.select-search__option')))
            except TimeoutException:
                metro_input.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.3)
                try:
                    option = WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, '.select-search__option')))
                except TimeoutException:
                    continue  

            option.click()  
            time.sleep(0.8)

            try:
                value = self.driver.find_element(By.CSS_SELECTOR, '.select-search__input').get_attribute('value')
            except NoSuchElementException:
                return True

            print(f"Попытка {attempt + 1}: в поле метро {value!r}")
            if value:
                return True

        return False

    # ---------- Шаг 1: «Для кого самокат» ----------

    def fill_order_form(self, first_name, last_name, address, metro, phone):
        self._close_cookies_banner()

        fields = [
            ((By.XPATH, '//input[@placeholder="* Имя"]'), first_name),
            ((By.XPATH, '//input[@placeholder="* Фамилия"]'), last_name),
            ((By.XPATH, '//input[contains(@placeholder, "Адрес")]'), address),
            ((By.XPATH, '//input[contains(@placeholder, "Телефон")]'), phone),
        ]
        for locator, value in fields:
            el = self.wait.until(EC.element_to_be_clickable(locator))
            el.clear()
            el.send_keys(value)

        if not self._select_metro(metro):
            raise AssertionError(f"Не удалось выбрать станцию метро: {metro}")

        try:
            self.driver.find_element(By.CSS_SELECTOR, '.select-search__input')
        except NoSuchElementException:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]')))
            print("Форма ушла на второй шаг сразу после выбора метро — «Далее» не нужен")
            return

        btn_next = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Далее"]')))
        btn_next.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]')))

    # ---------- Шаг 2: «Про аренду» ----------

    def fill_delivery_form(self):
        date_field = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//input[contains(@placeholder, "Когда привезти самокат")]')))
        date_field.click()

        today = date.today()
        day_xpath = (
            '//div[contains(@class, "react-datepicker__day")'
            ' and not(contains(@class, "--outside-month"))'
            ' and not(contains(@class, "--disabled"))'
            f' and normalize-space(text())="{today.day}"]'
        )
        day = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
        day.click()
        time.sleep(0.5)
        print("Дата в поле:", repr(date_field.get_attribute("value")))

        dd = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.Dropdown-control')))
        dd.click()
        opt = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.Dropdown-option')))
        opt.click()
        time.sleep(0.5)
        print("Аренда в поле:", repr(self.driver.find_element(By.CSS_SELECTOR, '.Dropdown-control').text))

    # ---------- Шаг 2: отправка ----------

    def _is_modal_open(self):
        return bool(self.driver.find_elements(
            By.XPATH, '//div[contains(@class, "Order_ModalHeader")]'))

    def _modal_state(self, driver):
        if driver.find_elements(By.XPATH, '//button[text()="Да"]'):
            return "confirm"
        if driver.find_elements(
            By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]'):
            return "success"
        return False

    def submit_order(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, '.Dropdown-option')
            self.driver.find_element(By.TAG_NAME, 'body').click()
            time.sleep(0.5)
            print("Дропдаун принудительно закрыт.")
        except NoSuchElementException:
            pass

        btn = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button.Button_Middle__1CSJM:nth-child(2)')))

        print("Кнопка Заказать — text:", repr(btn.text), "| class:", btn.get_attribute("class"))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.3)
        btn.click()

        state = WebDriverWait(self.driver, 10).until(self._modal_state)
        if state == "confirm":
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Да"]'))).click()

        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]')))
        print("Заказ успешно оформлен!")

    def check_success_message(self):
        element = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//div[contains(@class, "Order_ModalHeader") and contains(., "оформлен")]')))
        return element.text
