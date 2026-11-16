from .base_page import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def click_scooter_logo(self):
        self.click((By.CSS_SELECTOR, ".Header_LogoScooter__3lsAR"))

    def click_yandex_logo(self):
        self.click((By.CSS_SELECTOR, ".Header_LogoYandex__3TSOI"))

    def click_order_top(self):
        locator = (By.XPATH, '//button[contains(normalize-space(.), "Заказать")]')
        self.click(locator)

    def click_order_bottom(self):
        locator = (By.XPATH, '//button[contains(normalize-space(.), "Заказать")]')
        buttons = self.wait_for_presence_all(locator)
        btn = buttons[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

    def close_cookie_banner(self):
        try:
            btn = self.find_element((By.CSS_SELECTOR, ".App_CookieButton__3cvqF"))
            self.driver.execute_script("arguments[0].click();", btn)
        except NoSuchElementException:
            pass

    def open_faq_item(self, index):
        locator = (By.CSS_SELECTOR, ".accordion__item")
        self.wait_for_presence_all(locator)
        items = self.find_elements(locator)
        if index >= len(items):
            raise IndexError(f"Элемент FAQ с индексом {index} не найден. Всего: {len(items)}")
        element = items[index]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        item_locator = (By.CSS_SELECTOR, f".accordion__item:nth-child({index + 1})")
        self.click(item_locator)

    def get_answer_text(self, index):
        locator = (By.CSS_SELECTOR, f"[id^='accordion__panel-{index}']")
        panel = self.wait_for_visibility(locator)
        return panel.text