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
from function import DN_001, handle_alert

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Thanh toán sản phẩm thành công
def test_CKO_001(driver):
    # Steps
    DN_001(driver)
    time.sleep(2)
    driver.find_element(By.NAME, "themgiohang").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@href='index.php?quanli=thanhtoan']").click()
    payment_dropdown = driver.find_element(By.NAME, "payments")
    select = Select(payment_dropdown)
    select.select_by_visible_text("Thanh toán khi nhận hàng")
    driver.find_element(By.NAME, "thanhtoan").click()
    handle_alert(driver)
    # Expected result
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='alert alert-success p-2']"))
    )
    success_text = driver.find_element(By.XPATH, "//div[@class='alert alert-success p-2']").text
    assert "Đặt hàng thành công" in success_text


# Huỷ đơn hàng
def test_CKO_002(driver):
    # Step
    DN_001(driver)
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@href='index.php?quanli=dondamua']").click()
    # (By.XPATH, "//a[@href='?quanli=chitietdonmua&madonhang=9753']")
    driver.find_element(By.XPATH, "//a[text()='Xem']").click()
    driver.find_element(By.NAME, "huy_don_hang").click()
    handle_alert(driver)   
    # Expect result
    daHuy = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "btn-warning"))
    )
    
    assert daHuy.is_displayed