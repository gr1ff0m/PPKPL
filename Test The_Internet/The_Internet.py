import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os


class TestTheInternet:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def test_01_input_valid_number(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("123")
        assert input_field.get_attribute("value") == "123"

    def test_02_input_letter_should_not_work(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("abc")
        assert input_field.get_attribute("value") == ""

    def test_03_input_negative_number(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("-50")
        assert input_field.get_attribute("value") == "-50"

    def test_04_checkbox_check(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkbox = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']")[0]
        if not checkbox.is_selected():
            checkbox.click()
        assert checkbox.is_selected()

    def test_05_checkbox_uncheck(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkboxes = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']")
        for cb in checkboxes:
            if cb.is_selected():
                cb.click()
                assert not cb.is_selected()

    def test_06_select_dropdown_option(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))
        dropdown.select_by_value("1")
        assert dropdown.first_selected_option.text == "Option 1"

    def test_07_dropdown_default(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))
        assert dropdown.first_selected_option.text == "Please select an option"

    def test_08_login_success(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys(
            "SuperSecretPassword!")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "You logged into a secure area" in flash

    def test_09_login_wrong_password(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your password is invalid" in flash

    def test_10_login_wrong_username(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("wronguser")
        self.driver.find_element(By.ID, "password").send_keys(
            "SuperSecretPassword!")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid" in flash

    def test_11_login_empty(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()

        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid" in flash

    def test_12_upload_file_success(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")

        with open("test.txt", "w") as f:
            f.write("test content")

        file_input = self.driver.find_element(By.ID, "file-upload")
        file_input.send_keys(os.path.abspath("test.txt"))
        self.driver.find_element(By.ID, "file-submit").click()

        result = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "File Uploaded!" in result

        os.remove("test.txt")

    def test_13_upload_no_file(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")
        self.driver.find_element(By.ID, "file-submit").click()
        assert "upload" in self.driver.current_url

    def test_14_alert_ok(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()

        result = self.driver.find_element(By.ID, "result").text
        assert "You successfully clicked an alert" in result

    def test_15_confirm_ok(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsConfirm()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()

        result = self.driver.find_element(By.ID, "result").text
        assert "You clicked: Ok" in result

    def test_16_confirm_cancel(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsConfirm()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()

        result = self.driver.find_element(By.ID, "result").text
        assert "You clicked: Cancel" in result

    def test_17_prompt_with_text(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.send_keys("Hello")
        alert.accept()

        result = self.driver.find_element(By.ID, "result").text
        assert "You entered: Hello" in result

    def test_18_prompt_empty(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()

        result = self.driver.find_element(By.ID, "result").text
        assert "You entered:" in result

    def test_19_hover_over_image(self):
        self.driver.get("https://the-internet.herokuapp.com/hovers")
        avatar = self.driver.find_elements(By.CLASS_NAME, "figure")[0]
        ActionChains(self.driver).move_to_element(avatar).perform()

        caption = self.driver.find_element(
            By.CSS_SELECTOR, ".figcaption h5").text
        assert "user1" in caption

    def test_20_clear_input_field(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("12345")
        input_field.clear()
        assert input_field.get_attribute("value") == ""


if __name__ == "__main__":
    pytest.main(["-v", __file__])
