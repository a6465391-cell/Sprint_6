import allure # Если решите добавить шаги сюда (обычно не нужно, но для метода ниже можно)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver # Driver живет только здесь!
        self.wait = WebDriverWait(driver, 10)

    # --- БАЗОВЫЕ МЕТОДЫ (БЕЗ ALLURE) ---

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        # Стандартный клик
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def input_text(self, locator, text):
        el = self.wait_for_clickable(locator)
        el.clear()
        el.send_keys(text)

    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visibility(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
        
    def wait_for_presence_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def click_by_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def get_page_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url
        
    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def switch_to_main_tab(self, main_handle):
        self.driver.switch_to.window(main_handle)