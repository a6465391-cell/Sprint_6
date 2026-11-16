from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------- Кнопки заказа ----------

    def click_order_top(self):
        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(normalize-space(.), "Заказать")]')
        ))
        btn.click()

    def click_order_bottom(self):
        buttons = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//button[contains(normalize-space(.), "Заказать")]')
        ))
        btn = buttons[-1]  
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()


    def close_cookie_banner(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, ".App_CookieButton__3cvqF")
            self.driver.execute_script("arguments[0].click();", btn)
        except NoSuchElementException:
            pass

    # ---------- FAQ ----------

    def open_faq_item(self, index):
        self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".accordion__item")
        ))
        items = self.driver.find_elements(By.CSS_SELECTOR, ".accordion__item")
        if index >= len(items):
            raise IndexError(f"Элемент FAQ с индексом {index} не найден. Всего: {len(items)}")
        element = items[index]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f".accordion__item:nth-child({index + 1})")
        )).click()

    def get_answer_text(self, index):
        panel = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, f"[id^='accordion__panel-{index}']")
        ))
        return panel.text


