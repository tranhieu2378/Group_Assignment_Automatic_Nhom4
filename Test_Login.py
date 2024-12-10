import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function import open_login_modal, Login_Form, handle_alert, handle_message_input
from variable import emailValid, passwordValid, passwordInValid

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Testcase 1: Kiểm tra login thành công
def test_DN_001(driver):
    # Steps
    open_login_modal(driver)
    Login_Form(driver, emailValid, passwordValid)
    driver.find_element(By.NAME, "login_home").click()
    alert_text = handle_alert(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userDropdown"))
    )
    # Expected result
    assert "đăng nhập thành công" in alert_text
    assert "http://localhost/ASM_PHP1/index.php" in driver.current_url
    assert driver.find_element(By.ID, "userDropdown")


# Testcase 2: Kiểm tra login với tài khoản hoặc mật khẩu sai
def test_DN_002(driver):
    # Steps
    open_login_modal(driver)
    Login_Form(driver, emailValid, passwordInValid)
    driver.find_element(By.NAME, "login_home").click()
    alert_text = handle_alert(driver)
    # Expected result
    assert "Tài khoản hoặc mật khẩu sai" in alert_text


# Testcase 3: Kiểm tra login với form rỗng
def test_DN_003(driver):
    # Steps
    open_login_modal(driver)
    driver.find_element(By.NAME, "login_home").click()
    validation_message = handle_message_input(driver, "email_login")
    # Expected result
    assert "Please fill out this field" in validation_message


# Testcase 4: Kiểm tra login với email sai định dạng
def test_DN_004(driver):
    # Steps
    open_login_modal(driver)
    Login_Form(driver, "tranhieu123", "123456")
    driver.find_element(By.NAME, "login_home").click()
    validation_message = handle_message_input(driver, "email_login")
    # Expected result
    assert "Please include an '@' in the email address" or "Please enter an email address" in validation_message