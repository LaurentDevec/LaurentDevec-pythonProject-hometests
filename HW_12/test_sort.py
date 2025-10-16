import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helpers import is_page_available

URL = "https://demoqa.com/webtables"

def test_table_headers_sort_toggle_class(driver):
    if not is_page_available(URL):
        pytest.skip(f"Страница недоступна: {URL}")

    driver.get(URL)
    wait = WebDriverWait(driver, 8)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ReactTable")))
    headers = driver.find_elements(By.CSS_SELECTOR, "div.rt-th")
    assert headers

    for header in headers:
        before = header.get_attribute("class") or ""
        driver.execute_script("arguments[0].scrollIntoView(true);", header)
        header.click()
        wait.until(lambda d: (header.get_attribute("class") or "") != before)
        after = header.get_attribute("class") or ""
        assert before != after