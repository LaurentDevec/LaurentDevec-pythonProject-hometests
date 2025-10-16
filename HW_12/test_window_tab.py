import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helpers import is_page_available

URL = "https://demoqa.com/links"
EXPECTED_HREF_PREFIX = "https://demoqa.com/"

def test_home_link_opens_new_tab(driver):
    if not is_page_available(URL):
        pytest.skip(f"Страница недоступна: {URL}")

    driver.get(URL)
    wait = WebDriverWait(driver, 8)

    link = wait.until(EC.presence_of_element_located((By.ID, "simpleLink")))
    assert link.text.strip() == "Home"
    href = link.get_attribute("href")
    assert href is not None and href.startswith(EXPECTED_HREF_PREFIX)

    original_window = driver.current_window_handle
    link.click()
    wait.until(lambda d: len(d.window_handles) > 1)
    new_windows = [w for w in driver.window_handles if w != original_window]
    assert new_windows

    driver.switch_to.window(new_windows[0])
    wait.until(EC.url_contains("demoqa.com"))
