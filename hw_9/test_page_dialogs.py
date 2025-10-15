import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.modal_dialogs import ModalDialogsPage

class TestModalDialogs:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Настройка драйвера перед каждым тестом"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.set_window_size(1000, 1000)
        yield
        self.driver.quit()

    def test_modal_elements(self):
        """Тест проверки количества кнопок подменю"""
        # a. Перейти на страницу
        modal_page = ModalDialogsPage(self.driver)
        modal_page.open()

        # b. Проверить, что кнопок подменю - 5 шт
        buttons_count = modal_page.get_submenu_buttons_count()
        assert buttons_count == 5, f"Ожидалось 5 кнопок, но найдено {buttons_count}"

        print(f"✓ Найдено {buttons_count} кнопок подменю - тест пройден")

    def test_navigation_modal(self):
        """Тест навигации по модальным окнам"""
        # a. Перейти на страницу
        modal_page = ModalDialogsPage(self.driver)
        modal_page.open()

        # b. Обновить страницу
        modal_page.refresh_page()
        print("✓ Страница обновлена")

        # c. Перейти на главную страницу через иконку
        modal_page.click_main_icon()
        print("✓ Перешли на главную страницу через иконку")

        # d. Сделать шаг назад стрелкой браузера
        modal_page.go_back()
        print("✓ Сделали шаг назад")

        # e. Установить размеры экрана 900х400
        modal_page.set_window_size(900, 400)
        current_size = self.driver.get_window_size()
        print(f"✓ Установлен размер окна: {current_size['width']}x{current_size['height']}")

        # f. Сделать шаг вперед стрелкой браузера
        modal_page.go_forward()
        print("✓ Сделали шаг вперед")

        # g. Вызвать проверку урла на главной странице
        current_url = modal_page.get_current_url()
        expected_url = "https://demoqa.com/"
        assert current_url == expected_url, f"URL не совпадает. Ожидалось: {expected_url}, получено: {current_url}"
        print(f"✓ URL верный: {current_url}")

        # h. Проверить title на главной
        page_title = modal_page.get_page_title()
        expected_title = "DEMOQA"
        assert expected_title in page_title, f"Title не совпадает. Ожидалось: {expected_title}, получено: {page_title}"
        print(f"✓ Title верный: {page_title}")

        # i. Вернуть размеры экрана по умолчанию 1000x1000
        modal_page.set_window_size(1000, 1000)
        final_size = self.driver.get_window_size()
        print(f"✓ Возвращен размер по умолчанию: {final_size['width']}x{final_size['height']}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])