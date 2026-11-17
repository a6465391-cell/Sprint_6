import pytest
from selenium import webdriver
from selenium.webdriver.firefox import service as ff_service

@pytest.fixture
def driver():
    service = ff_service.Service(executable_path="geckodriver.exe")
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    yield driver  
    driver.quit()  