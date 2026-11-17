import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from .base_page import BasePage

class MainPage(BasePage):
    
    LOCATOR_LOGO_SCOOTER = (By.CSS_SELECTOR, ".Header_LogoScooter__3lsAR")
    LOCATOR_LOGO_YANDEX = (By.CSS_SELECTOR, ".Header_LogoYandex__3TSOI")
    LOCATOR_ORDER_BUTTON = (By.XPATH, '//button[contains(normalize-space(.), "Заказать")]')
    LOCATOR_COOKIE_BTN = (By.CSS_SELECTOR, ".App_CookieButton__3cvqF")
    LOCATOR_FAQ_ITEM = (By.CSS_SELECTOR, ".accordion__item")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Клик по логотипу самоката")
    def click_scooter_logo(self):
        self.click(self.LOCATOR_LOGO_SCOOTER)

    @allure.step("Клик по логотипу Яндекса")
    def click_yandex_logo(self):
        self.click(self.LOCATOR_LOGO_YANDEX)

    @allure.step("Клик по кнопке «Заказать» (верхняя)")
    def click_order_top(self):
        self.click(self.LOCATOR_ORDER_BUTTON)

    @allure.step("Клик по кнопке «Заказать» (нижняя)")
    def click_order_bottom(self):

        buttons = self.wait_for_presence_all(self.LOCATOR_ORDER_BUTTON)
        if not buttons:
            raise AssertionError("Кнопки заказа не найдены на странице")
        
        btn = buttons[-1]  
        
        self.scroll_to_element(btn)
        
        self.click_by_js(btn)

    @allure.step("Закрытие баннера с куки")
    def close_cookie_banner(self):
        try:
            btn = self.find_element(self.LOCATOR_COOKIE_BTN)
            self.click_by_js(btn)
        except NoSuchElementException:
            pass

    @allure.step("Открытие пункта FAQ по индексу")
    def open_faq_item(self, index):
        self.wait_for_presence_all(self.LOCATOR_FAQ_ITEM)
        items = self.find_elements(self.LOCATOR_FAQ_ITEM)
        
        if index >= len(items):
            raise IndexError(f"Элемент FAQ не найден. Всего: {len(items)}")
        
        element = items[index]
        # Используем метод из BasePage
        self.scroll_to_element(element)
        element.click() 

    @allure.step("Получение текста ответа из FAQ по индексу")
    def get_answer_text(self, index):
        # Динамический локатор (допустимо в методах страниц)
        locator = (By.CSS_SELECTOR, f"[id^='accordion__panel-{index}']")
        panel = self.wait_for_visibility(locator)
        return panel.text