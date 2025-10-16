import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def chrome_options():
    opts = Options()
    opts.add_argument("--window-size=1200,900")
    return opts

@pytest.fixture(scope="function")
def driver(chrome_options):
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=chrome_options)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass
