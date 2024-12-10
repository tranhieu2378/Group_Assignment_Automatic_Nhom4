import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import random
from function import DN_001, clear_field, DN_002, navigate_qlnd, Update_Profile_Form, Update_Password_Form, verify_updated_information
from variable import nameProf, phoneProf, addressProf, odlPwd, duplicatePwd, shortPwd, emailChange, pwdChange

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Cập nhật thông tin
def test_UIF_001(driver):
    # Step
    DN_001(driver)
    navigate_qlnd(driver)

    updateProfile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='index.php?quanli=suathongtin']"))
    )
    updateProfile_button.click()

    name_element = driver.find_element(By.NAME, "name_user")
    address_element = driver.find_element(By.NAME, "address_user")
    phone_element = driver.find_element(By.NAME, "phone_user")
    clear_field(name_element)
    clear_field(address_element)
    clear_field(phone_element)

    Update_Profile_Form(driver, nameProf, addressProf, phoneProf)

    driver.find_element(By.NAME, "doithongtin").click()
    # Expected result
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-primary"))
    )
    assert "Thay đổi thông tin thành công" in success_message.text
    verify_updated_information(driver, nameProf, addressProf, phoneProf)


# Cập nhật thông tin để form rỗng
def test_UIF_002(driver):
    DN_001(driver)
    navigate_qlnd(driver)

    updateProfile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='index.php?quanli=suathongtin']"))
    )
    updateProfile_button.click()

    name_element = driver.find_element(By.NAME, "name_user")
    address_element = driver.find_element(By.NAME, "address_user")
    phone_element = driver.find_element(By.NAME, "phone_user")
    clear_field(name_element)
    clear_field(address_element)
    clear_field(phone_element)

    driver.find_element(By.NAME, "doithongtin").click()

    # Expected result
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
    )
    assert "Vui lòng điền đầy đủ tất cả các thông tin." in success_message.text


# Cập nhật mật khẩu thành công
def test_UIF_003(driver):
    # Step
    DN_002(driver, emailChange, "1234567")
    navigate_qlnd(driver)
    driver.find_element(By.XPATH, "//a[@href='index.php?quanli=doimatkhau']").click()

    Update_Password_Form(driver, "1234567", "123456", "123456")
    time.sleep(2)
    driver.find_element(By.NAME, "doimatkhau").click()
    # Expected result
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-primary"))
    )
    assert "Thay đổi mật khẩu thành công" in success_message.text
    DN_002(driver, emailChange, "123456")


# Cập nhật mật khẩu với mật khẩu mới trùng mật khẩu cũ
def test_UIF_004(driver):
    # Step 1: Đăng nhập
    DN_002(driver, "tranhieu123@gmail.com", "123456")
    navigate_qlnd(driver)

    # Step 4: Nhấn nút đổi mật khẩu
    updateProfile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='index.php?quanli=doimatkhau']"))
    )
    updateProfile_button.click()
    # Step 5: Điền form
    Update_Password_Form(driver, odlPwd, duplicatePwd, duplicatePwd)
    # Step 6: Nhấn đổi mk
    driver.find_element(By.NAME, "doimatkhau").click()

    # Expected result
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
    )
    assert "Mật khẩu mới không được giống mật khẩu cũ" in success_message.text


# Cập nhật mật khẩu khi mật khẩu mới dưới 6 ký tự và xác nhận mật khẩu không khớp
def test_UIF_005(driver):
    # Step 1: Đăng nhập
    DN_002(driver, "tranhieu123@gmail.com", "123456")
    navigate_qlnd(driver)
    # Step 4: Nhấn nút đổi mật khẩu
    updateProfile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='index.php?quanli=doimatkhau']"))
    )
    updateProfile_button.click()
    # Step 5: Điền form
    Update_Password_Form(driver, odlPwd, shortPwd, duplicatePwd)

    # Step 6: Nhấn đổi mk
    driver.find_element(By.NAME, "doimatkhau").click()

    # Expected result
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
    )
    assert "Mật khẩu mới phải trên 6 ký tự" in success_message.text
    assert "Nhập lại mật khẩu không giống nhau" in success_message.text