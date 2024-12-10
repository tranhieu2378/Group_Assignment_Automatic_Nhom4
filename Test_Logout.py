import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from function import DN_001, handle_alert
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Testcase 1: Đăng xuất thành công
def test_DX_001(driver):
    # Steps
    # 1
    DN_001(driver)
    # 2
    user_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userDropdown"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(user_dropdown).perform()
    # 3
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='?logout=1']"))
    )
    logout_button.click()
    # 4
    alert_text = handle_alert(driver)
    # Expected result
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "w3view-cart"))
    )
    assert "Đăng xuất thành công" in alert_text
    assert "http://localhost/ASM_PHP1/index.php" in driver.current_url
    assert driver.find_element(By.CLASS_NAME, "w3view-cart")