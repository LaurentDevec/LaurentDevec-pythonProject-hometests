.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.helpers import is_page_available

URL = "https://demoqa.com/alerts"

def test_timer_alert_shows(driver):
    if not is_page_available(URL):
        pytest.skip(f"Страница недоступна: {URL}")

    driver.get(URL)
    wait = WebDriverWait(driver, 12)

    btn = wait.until(EC.element_to_be_clickable((By.ID, "timerAlertButton")))
    btn.click()
    alert = wait.until(EC.alert_is_present())
    assert alert is not None
    alert.accept()
