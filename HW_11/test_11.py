import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class TestWebTables:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://demoqa.com/webtables")
        self.wait = WebDriverWait(self.driver, 10)

        # Устанавливаем количество строк в таблице = 5
        select_element = self.driver.find_element(By.CSS_SELECTOR, "select[aria-label='rows per page']")
        select = Select(select_element)
        select.select_by_value("5")
        time.sleep(1)

    def teardown_method(self):
        self.driver.quit()

    def test_initial_state(self):
        """Тест начального состояния - кнопки Next и Previous заблокированы"""
        # Проверяем, что кнопки заблокированы и имеют атрибут disabled
        next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
        previous_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Previous']")

        assert "disabled" in next_button.get_attribute("class"), "Кнопка Next должна быть заблокирована"
        assert "disabled" in previous_button.get_attribute("class"), "Кнопка Previous должна быть заблокирована"

        # Проверяем, что по клику ничего не происходит
        current_page_info = self.driver.find_element(By.CSS_SELECTOR, "span[aria-live='polite']").text

        next_button.click()
        time.sleep(0.5)
        assert self.driver.find_element(By.CSS_SELECTOR, "span[aria-live='polite']").text == current_page_info

        previous_button.click()
        time.sleep(0.5)
        assert self.driver.find_element(By.CSS_SELECTOR, "span[aria-live='polite']").text == current_page_info

    def add_record(self, first_name, last_name, email, age, salary, department):
        """Вспомогательная функция для добавления записи"""
        # Нажимаем кнопку Add
        add_button = self.driver.find_element(By.ID, "addNewRecordButton")
        add_button.click()

        # Ждем появления диалога
        dialog = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))

        # Заполняем форму
        self.driver.find_element(By.ID, "firstName").send_keys(first_name)
        self.driver.find_element(By.ID, "lastName").send_keys(last_name)
        self.driver.find_element(By.ID, "userEmail").send_keys(email)
        self.driver.find_element(By.ID, "age").send_keys(age)
        self.driver.find_element(By.ID, "salary").send_keys(salary)
        self.driver.find_element(By.ID, "department").send_keys(department)

        # Нажимаем Submit
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

        # Ждем закрытия диалога
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-content")))

    def test_add_three_records_and_pagination(self):
        """Тест добавления 3 записей и работы пагинации"""
        # Добавляем 3 записи
        test_data = [
            ("John", "Doe", "john@test.com", "30", "50000", "IT"),
            ("Jane", "Smith", "jane@test.com", "25", "60000", "Marketing"),
            ("Bob", "Johnson", "bob@test.com", "35", "70000", "Sales")
        ]

        for data in test_data:
            self.add_record(*data)
            time.sleep(1)

        # Проверяем, что появилась 2-я страница (of 2)
        page_info = self.driver.find_element(By.CSS_SELECTOR, "span[aria-live='polite']").text
        assert "of 2" in page_info, f"Должно быть 'of 2', но получили: {page_info}"

        # Проверяем, что кнопка Next стала доступной
        next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
        assert "disabled" not in next_button.get_attribute("class"), "Кнопка Next должна быть доступной"

        # Кликаем по кнопке Next - открывается 2-я страница
        next_button.click()
        time.sleep(1)

        # Проверяем, что мы на второй странице
        current_page_info = self.driver.find_element(By.CSS_SELECTOR, "span[aria-live='polite']").text
        assert "Page 2" in current_page_info or "2 of 2" in current_page_info

        # Проверяем, что кнопка Previous доступна
        previous_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Previous']")
        assert "disabled" not in previous_button.get_attribute("class"), "Кнопка Previous должна быть доступной"

        # Кликаем по кнопке Previous - открывается 1-я страница
        previous_button.click()
        time.sleep(1)

        # Проверяем, что мы на первой странице
        current_page_info = self.driver.find_element(By.CSS_SELECTOR, "span[aria-live='polite']").text
        assert "Page 1" in current_page_info or "1 of 2" in current_page_info

    def test_edit_record(self):
        """Тест редактирования записи"""
        # Находим первую запись и кликаем на карандаш
        edit_button = self.driver.find_element(By.CSS_SELECTOR, "span[title='Edit']")
        edit_button.click()

        # Ждем появления диалога
        dialog = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))

        # Меняем имя
        first_name_field = self.driver.find_element(By.ID, "firstName")
        first_name_field.clear()
        first_name_field.send_keys("UpdatedName")

        # Сохраняем
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

        # Ждем закрытия диалога
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-content")))

        # Проверяем, что данные обновились в таблице
        time.sleep(1)
        first_name_cell = self.driver.find_element(By.CSS_SELECTOR, ".rt-tbody .rt-tr:first-child .rt-td:nth-child(1)")
        assert first_name_cell.text == "UpdatedName"

    def test_delete_record(self):
        """Тест удаления записи"""
        # Запоминаем количество записей до удаления
        rows_before = len(self.driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr:not(.padRow)"))

        # Находим первую запись и кликаем на корзину
        delete_button = self.driver.find_element(By.CSS_SELECTOR, "span[title='Delete']")
        delete_button.click()

        time.sleep(1)

        # Проверяем, что запись удалилась
        rows_after = len(self.driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr:not(.padRow)"))
        assert rows_after == rows_before - 1

    def test_empty_form_validation(self):
        """Тест валидации пустой формы"""
        # Нажимаем кнопку Add
        add_button = self.driver.find_element(By.ID, "addNewRecordButton")
        add_button.click()

        # Ждем появления диалога
        dialog = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-content")))

        # Пытаемся сохранить пустую форму
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

        # Проверяем, что диалог не закрылся (форма не прошла валидацию)
        time.sleep(1)
        assert self.driver.find_element(By.CLASS_NAME, "modal-content").is_displayed()

        # Закрываем диалог
        close_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
        close_button.click()

if __name__ == "__main__":
    # Запуск тестов
    test = TestWebTables()
    test.setup_method()

    try:
        test.test_initial_state()
        print("✓ test_initial_state passed")

        test.test_add_three_records_and_pagination()
        print("✓ test_add_three_records_and_pagination passed")

        test.test_edit_record()
        print("✓ test_edit_record passed")

        test.test_delete_record()
        print("✓ test_delete_record passed")

        test.test_empty_form_validation()
        print("✓ test_empty_form_validation passed")

        print("\nВсе тесты прошли успешно!")

    except Exception as e:
        print(f"✗ Тест упал с ошибкой: {e}")

    finally:
        test.teardown_method()