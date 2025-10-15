import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # если нужен безголовый режим

    driver = webdriver.Chrome(options=chrome_options)  # убедись, что chromedriver в PATH
    yield driver
    driver.quit()