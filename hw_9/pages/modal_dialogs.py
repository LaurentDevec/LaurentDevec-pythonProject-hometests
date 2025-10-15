import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ModalDialogsPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://demoqa.com/modal-dialogs"

        # Локаторы
        self.submenu_buttons = (By.CSS_SELECTOR, "div.element-list.collapse.show li.btn-light")
        self.main_icon = (By.CSS_SELECTOR, "header a img")

    def open(self):
        """Открыть страницу модальных окон"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.submenu_buttons)
        )
        return self

    def get_submenu_buttons_count(self):
        """Получить количество кнопок подменю"""
        buttons = self.driver.find_elements(*self.submenu_buttons)
        return len(buttons)

    def refresh_page(self):
        """Обновить страницу"""
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.submenu_buttons)
        )
        return self

    def click_main_icon(self):
        """Кликнуть по главной иконке"""
        self.driver.find_element(*self.main_icon).click()
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("https://demoqa.com/")
        )
        return self

    def go_back(self):
        """Шаг назад в браузере"""
        self.driver.back()
        return self

    def go_forward(self):
        """Шаг вперед в браузере"""
        self.driver.forward()
        return self

    def set_window_size(self, width, height):
        """Установить размеры окна браузера"""
        self.driver.set_window_size(width, height)
        return self

    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Получить заголовок страницы"""
        return self.driver.title