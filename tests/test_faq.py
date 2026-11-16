import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from page_objects.main_page import MainPage

@allure.epic("Яндекс.Самокат")
@allure.feature("FAQ")
@pytest.mark.parametrize("faq_index", range(6))
def test_faq_items(faq_index):
    service = Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)
    
    try:
        page = MainPage(driver)
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        page.open_faq_item(faq_index)
        text = page.get_answer_text(faq_index)
        
        assert text.strip() != "", f"Пустой ответ для пункта {faq_index}"
    finally:
        driver.quit()
