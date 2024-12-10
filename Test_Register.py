import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from function import open_register_modal, Register_Form, handle_alert
from variable import emailRegis, nameRegis, phoneRegis, passwordRegis, addressRegis, emailValid, emailInValid, phoneInvalid, shortPwd

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Testcase 1: Đăng ký thành công -- Chưa test vì 2 driver test chung không được
def test_DK_001(driver):
    # Steps
    open_register_modal(driver)
    Register_Form(driver, nameRegis, emailRegis, phoneRegis, addressRegis, passwordRegis)
    driver.find_element(By.NAME, "register").click()
    # Expected result
    alert_text = handle_alert(driver)
    assert "Đăng ký thành công. Mời bạn đăng nhập" in alert_text
    assert "http://localhost/ASM_PHP1/index.php" in driver.current_url


# Testcase 2: Đăng ký khi trùng tài khoản
def test_DK_002(driver):
    # Steps
    open_register_modal(driver)
    Register_Form(driver, nameRegis, emailValid, phoneRegis, addressRegis, passwordRegis)
    driver.find_element(By.NAME, "register").click()
    # Expected result
    alert_text = handle_alert(driver)
    assert "Email đã được sử dụng. Vui lòng chọn email khác." in alert_text


# Testcase 3: Đăng ký khi để form rỗng
def test_DK_003(driver):
    # Steps
    open_register_modal(driver)
    driver.find_element(By.NAME, "register").click()
    # Expected result
    hoTen_field = driver.find_element(By.NAME, "register_name")
    validation_message = driver.execute_script("return arguments[0].validationMessage;", hoTen_field)
    assert "Please fill out this field" in validation_message


# Testcase 4: Đăng ký khi nhập sai định dạng Email
def test_DK_004(driver):
    # Steps
    open_register_modal(driver)
    Register_Form(driver, nameRegis, emailInValid, phoneRegis, addressRegis, passwordRegis)
    driver.find_element(By.NAME, "register").click()
    # Expected result
    email_field = driver.find_element(By.NAME, "register_email")
    validation_message = driver.execute_script("return arguments[0].validationMessage;", email_field)
    assert "Please include an '@' in the email address" or "Please enter an email address" in validation_message


# Testcase 5: Đăng ký khi nhập sai định dạng số điện thoại
def test_DK_005(driver):
    # Steps
    open_register_modal(driver)
    Register_Form(driver, nameRegis, emailRegis, phoneInvalid, addressRegis, passwordRegis)
    driver.find_element(By.NAME, "register").click()
    # Expected result
    phone_field = driver.find_element(By.NAME, "register_phone")
    validation_message = driver.execute_script("return arguments[0].validationMessage;", phone_field)
    title_attribute = phone_field.get_attribute("title")
    assert "Please match the requested format" in validation_message
    assert "Vui lòng nhập số hợp lệ" in title_attribute


# Testcase 6: Đăng ký khi mật khẩu dưới 6 ký tự
def test_DK_006(driver):
    # Steps
    open_register_modal(driver)
    Register_Form(driver, nameRegis, emailRegis, phoneRegis, addressRegis, shortPwd)
    driver.find_element(By.NAME, "register").click()
    # Expected result
    password_field = driver.find_element(By.NAME, "register_password")
    validation_message = driver.execute_script("return arguments[0].validationMessage;", password_field)
    assert "Please lengthen this text to 6 characters or more" or "Please use at least 6 characters" in validation_message