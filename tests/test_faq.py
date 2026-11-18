import pytest
import allure
from page_objects.main_page import MainPage

@allure.epic("Яндекс.Самокат")
@allure.feature("FAQ")
class TestFaq:

    @allure.story("Проверка пунктов FAQ (индекс {faq_index})")  
    @pytest.mark.parametrize("faq_index", range(6))
    def test_faq_items(self, faq_index, driver):
        page = MainPage(driver)
        driver.get("https://qa-scooter.praktikum-services.ru/")
        
        page.close_cookie_banner()
        
        question_text = page.get_question_text(faq_index)
        assert question_text, f"Не удалось получить текст вопроса для индекса {faq_index}"
        
        page.open_faq_item(faq_index)
        
        answer_text = page.get_answer_text(faq_index)
        assert answer_text.strip(), f"Пустой ответ для вопроса: '{question_text}'" 
