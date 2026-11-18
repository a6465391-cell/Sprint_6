import pytest
from selenium import webdriver
from selenium.webdriver.firefox import service as ff_service
from selenium.webdriver.firefox.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.set_preference("layers.acceleration.force-enabled", False)
    
    service = ff_service.Service(executable_path="geckodriver.exe")
    
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver

    driver.quit()
   