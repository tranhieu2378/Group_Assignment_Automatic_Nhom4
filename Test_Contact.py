import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from function import Contact_Form, handle_alert, handle_message_input, navigate_contact
from variable import contactName, contactMessage, contactEmail, emailInValid

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Testcase 1: Liên hệ thành công
def test_LH_001(driver):
    navigate_contact(driver)
    Contact_Form(driver, contactName, contactEmail, contactMessage)
    driver.find_element(By.CLASS_NAME, "contact-form").find_element(By.TAG_NAME, "input").click()
    # Expected result
    alert_text = handle_alert(driver)
    assert "Tin nhắn đã được gửi thành công!" in alert_text


# Testcase 2: Liên hệ khi để rỗng tên và email
def test_LH_002(driver):
    navigate_contact(driver)
    # Test rỗng họ tên
    driver.find_element(By.CLASS_NAME, "contact-form").find_element(By.TAG_NAME, "input").click()
    validation_message = handle_message_input(driver, "Name")
    # Expected result 1
    assert "Please fill out this field" in validation_message

    Contact_Form(driver, contactName, "", contactMessage)
    # Test rỗng email
    driver.find_element(By.CLASS_NAME, "contact-form").find_element(By.TAG_NAME, "input").click()
    validation_message = handle_message_input(driver, "Email")
    # Expected result 2
    assert "Please fill out this field" in validation_message


# Testcase 3: Liên hệ khi nhập sai định dạng Email
def test_LH_003(driver):
    navigate_contact(driver)
    # Step 3: Điền form
    Contact_Form(driver, contactName, emailInValid, contactMessage)
    # Step 4: Click
    driver.find_element(By.CLASS_NAME, "contact-form").find_element(By.TAG_NAME, "input").click()
    # Expected result
    validation_message =  handle_message_input(driver, "Email")
    assert "Please include an '@' in the email address" or "Please enter an email address" in validation_message