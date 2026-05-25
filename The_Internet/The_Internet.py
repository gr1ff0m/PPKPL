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

    # ==================== 20 TEST POSITIF ====================

    def test_01_input_valid_number(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("500")
        assert input_field.get_attribute("value") == "500"

    def test_02_input_zero(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("0")
        assert input_field.get_attribute("value") == "0"

    def test_03_input_negative_number(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("-100")
        assert input_field.get_attribute("value") == "-100"

    def test_04_input_decimal_number(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("3.14")
        assert input_field.get_attribute("value") == "3.14"

    def test_05_clear_input_field(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("12345")
        input_field.clear()
        assert input_field.get_attribute("value") == ""

    def test_06_checkbox_check(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkbox = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']")[0]
        if not checkbox.is_selected():
            checkbox.click()
        assert checkbox.is_selected()

    def test_07_checkbox_uncheck(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkboxes = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']")
        for cb in checkboxes:
            if cb.is_selected():
                cb.click()
                assert not cb.is_selected()

    def test_08_select_dropdown_option1(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))
        dropdown.select_by_value("1")
        assert dropdown.first_selected_option.text == "Option 1"

    def test_09_select_dropdown_option2(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))
        dropdown.select_by_value("2")
        assert dropdown.first_selected_option.text == "Option 2"

    def test_10_login_success(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys(
            "SuperSecretPassword!")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "You logged into a secure area" in flash

    def test_11_upload_file_success(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")
        with open("test.txt", "w") as f:
            f.write("test content")
        file_input = self.driver.find_element(By.ID, "file-upload")
        file_input.send_keys(os.path.abspath("test.txt"))
        self.driver.find_element(By.ID, "file-submit").click()
        result = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "File Uploaded!" in result
        os.remove("test.txt")

    def test_12_alert_ok(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()
        result = self.driver.find_element(By.ID, "result").text
        assert "You successfully clicked an alert" in result

    def test_13_confirm_ok(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsConfirm()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()
        result = self.driver.find_element(By.ID, "result").text
        assert "You clicked: Ok" in result

    def test_14_confirm_cancel(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsConfirm()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()
        result = self.driver.find_element(By.ID, "result").text
        assert "You clicked: Cancel" in result

    def test_15_prompt_with_text(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.send_keys("Hello")
        alert.accept()
        result = self.driver.find_element(By.ID, "result").text
        assert "You entered: Hello" in result

    def test_16_hover_first_image(self):
        self.driver.get("https://the-internet.herokuapp.com/hovers")
        avatar = self.driver.find_elements(By.CLASS_NAME, "figure")[0]
        ActionChains(self.driver).move_to_element(avatar).perform()
        caption = self.driver.find_element(
            By.CSS_SELECTOR, ".figcaption h5").text
        assert "user1" in caption

    def test_17_checkbox_default_state(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkboxes = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']")
        assert checkboxes[0].is_selected() == False

    def test_18_add_remove_elements(self):
        self.driver.get(
            "https://the-internet.herokuapp.com/add_remove_elements/")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='addElement()']").click()
        delete_button = self.driver.find_element(
            By.CLASS_NAME, "added-manually")
        assert delete_button.is_displayed()

    def test_19_key_press_space(self):
        self.driver.get("https://the-internet.herokuapp.com/key_presses")
        target = self.driver.find_element(By.ID, "target")
        target.click()
        target.send_keys(Keys.SPACE)
        import time
        time.sleep(0.5)
        result = self.driver.execute_script(
            "return document.getElementById('result').innerText;")
        assert "SPACE" in result

    def test_20_key_press_tab(self):
        self.driver.get("https://the-internet.herokuapp.com/key_presses")
        target = self.driver.find_element(By.ID, "target")
        target.click()
        target.send_keys(Keys.TAB)
        import time
        time.sleep(0.5)
        result = self.driver.execute_script(
            "return document.getElementById('result').innerText;")
        assert "TAB" in result

    # ==================== 20 TEST NEGATIF ====================

    def test_21_input_letter_not_valid(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("abc")
        assert input_field.get_attribute("value") == ""

    def test_22_input_special_characters(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("@#$%")
        assert input_field.get_attribute("value") == ""

    def test_23_status_code_200(self):
        self.driver.get("https://the-internet.herokuapp.com/status_codes")
        self.driver.find_element(By.LINK_TEXT, "200").click()
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        assert "This page returned a 200 status code" in body_text

    def test_24_input_very_long(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        long_input = "1" * 200
        input_field.send_keys(long_input)
        assert input_field.get_attribute("value") is not None

    def test_25_login_wrong_password(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your password is invalid" in flash

    def test_26_login_wrong_username(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("wronguser")
        self.driver.find_element(By.ID, "password").send_keys(
            "SuperSecretPassword!")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid" in flash

    def test_27_login_empty_username(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "password").send_keys(
            "SuperSecretPassword!")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid" in flash

    def test_28_login_empty_password(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your password is invalid" in flash

    def test_29_login_empty_all(self):
        self.driver.get("https://the-internet.herokuapp.com/login")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        flash = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))).text
        assert "Your username is invalid" in flash

    def test_30_upload_no_file(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")
        self.driver.find_element(By.ID, "file-submit").click()
        assert "upload" in self.driver.current_url

    def test_31_upload_empty_file(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")
        with open("empty.txt", "w") as f:
            pass
        file_input = self.driver.find_element(By.ID, "file-upload")
        file_input.send_keys(os.path.abspath("empty.txt"))
        self.driver.find_element(By.ID, "file-submit").click()
        result = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "File Uploaded!" in result
        os.remove("empty.txt")

    def test_32_upload_non_txt_file(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")
        with open("test.jpg", "w") as f:
            f.write("fake jpg content")
        file_input = self.driver.find_element(By.ID, "file-upload")
        file_input.send_keys(os.path.abspath("test.jpg"))
        self.driver.find_element(By.ID, "file-submit").click()
        result = self.driver.find_element(By.TAG_NAME, "h3").text
        assert "File Uploaded!" in result
        os.remove("test.jpg")

    def test_33_prompt_empty(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.accept()
        result = self.driver.find_element(By.ID, "result").text
        assert "You entered:" in result

    def test_34_prompt_cancel(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        self.driver.find_element(
            By.CSS_SELECTOR, "button[onclick='jsPrompt()']").click()
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()
        result = self.driver.find_element(By.ID, "result").text
        assert "You entered: null" in result

    def test_35_dropdown_default(self):
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))
        assert dropdown.first_selected_option.text == "Please select an option"

    def test_36_checkbox_double_click(self):
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        checkbox = self.driver.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox']")[0]
        initial_state = checkbox.is_selected()
        checkbox.click()
        checkbox.click()
        assert checkbox.is_selected() == initial_state

    def test_37_broken_images(self):
        self.driver.get("https://the-internet.herokuapp.com/broken_images")
        images = self.driver.find_elements(By.TAG_NAME, "img")
        broken_found = False
        for img in images:
            width = self.driver.execute_script(
                "return arguments[0].naturalWidth", img)
            if width == 0:
                broken_found = True
                break
        assert broken_found == True

    def test_38_key_press_unknown(self):
        self.driver.get("https://the-internet.herokuapp.com/key_presses")
        target = self.driver.find_element(By.ID, "target")
        target.click()
        target.send_keys(Keys.F1)
        import time
        time.sleep(0.5)
        result = self.driver.execute_script(
            "return document.getElementById('result').innerText;")
        assert result is not None

    def test_39_backspace_delete(self):
        self.driver.get("https://the-internet.herokuapp.com/inputs")
        input_field = self.driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("12345")
        input_field.send_keys(Keys.BACKSPACE)
        assert input_field.get_attribute("value") == "1234"

    def test_40_basic_auth(self):
        self.driver.get(
            "https://admin:admin@the-internet.herokuapp.com/basic_auth")
        success_text = self.driver.find_element(By.TAG_NAME, "p").text
        assert "Congratulations" in success_text


if __name__ == "__main__":
    pytest.main(["-v", __file__])
