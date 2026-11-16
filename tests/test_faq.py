import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By  # <-- ЭТОГО НЕ ХВАТАЛО
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page_objects.main_page import MainPage

@allure.epic("Яндекс.Самокат")
@allure.feature("FAQ")
@pytest.mark.parametrize("faq_index", range(6))
def test_faq_items(faq_index):
    service = Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)
    wait = WebDriverWait(driver, 10)
    
    page = MainPage(driver)

    try:
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        # Ждем появления элементов FAQ
        wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".accordion__item")) > 0)
        
        # Открываем пункт
        page.open_faq_item(faq_index)
        
        # Ждем появления текста
        wait.until(lambda d: page.get_answer_text(faq_index).strip() != "")
        
        text = page.get_answer_text(faq_index)
        assert text.strip() != "", f"Пустой ответ для пункта {faq_index}"
        
    finally:
        driver.quit()
