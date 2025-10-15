import time
import pytest
from pages.accordion import Accordion

@pytest.mark.ui
def test_visible_accordion(browser):
    page = Accordion(browser)
    page.open()

    # Проверка что элемент виден
    assert page.is_section1_content_visible(), "Section1 content должен быть виден"

    # Клик по заголовку
    page.click_section1()
    time.sleep(2)

    # Проверка что элемент теперь НЕ виден
    assert not page.is_section1_content_visible(), "Section1 content должен быть скрыт после клика"

@pytest.mark.ui
def test_visible_accordion_default(browser):
    page = Accordion(browser)
    page.open()

    # Проверка что элементы по умолчанию скрыты
    assert not page.is_section2_content1_visible(), "Section2 content 1 должен быть скрыт"
    assert not page.is_section2_content2_visible(), "Section2 content 2 должен быть скрыт"
    assert not page.is_section3_content_visible(), "Section3 content должен быть скрыт"