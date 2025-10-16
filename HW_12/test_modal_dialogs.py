import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helpers import is_page_available

URL = "https://demoqa.com/modal-dialogs"

def test_modal_open_close(driver):
    if not is_page_available(URL):
        pytest.skip(f"Страница недоступна: {URL}")

    driver.get(URL)
    wait = WebDriverWait(driver, 8)

    small_btn = wait.until(EC.element_to_be_clickable((By.ID, "showSmallModal")))
    small_btn.click()
    small_title_locator = (By.ID, "example-modal-sizes-title-sm")
    small_title = wait.until(EC.visibility_of_element_located(small_title_locator))
    assert small_title.is_displayed()
    close_small = driver.find_element(By.ID, "closeSmallModal")
    close_small.click()
    wait.until(EC.invisibility_of_element_located(small_title_locator))

    large_btn = wait.until(EC.element_to_be_clickable((By.ID, "showLargeModal")))
    large_btn.click()
    large_title_locator = (By.ID, "example-modal-sizes-title-lg")
    large_title = wait.until(EC.visibility_of_element_located(large_title_locator))
    assert large_title.is_displayed()
    close_large = driver.find_element(By.ID, "closeLargeModal")
    close_large.click()
    wait.until(EC.invisibility_of_element_located(large_title_locator))
