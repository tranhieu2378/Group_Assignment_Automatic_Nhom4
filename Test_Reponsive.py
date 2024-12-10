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
from function import DN_001, clear_field, open_login_modal, DN_002
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_RPS_001(driver):
    # Step 1
    driver.get("http://localhost/ASM_PHP1/index.php")
    # Step 2
    driver.set_window_size(375, 667)
    # Expected result
    navbar_toggler = driver.find_element(By.CLASS_NAME, "navbar-toggler")
    time.sleep(1)
    assert navbar_toggler.is_displayed()


def test_RPS_002(driver):
    # Step 1
    driver.get("http://localhost/ASM_PHP1/index.php")
    # Step 2
    driver.set_window_size(375, 667)
    # Step 3
    navbar_toggler = driver.find_element(By.CLASS_NAME, "navbar-toggler")
    navbar_toggler.click()
    time.sleep(1)

    # Expected result
    navbar_content = driver.find_element(By.ID, "navbarSupportedContent")
    assert navbar_content.is_displayed()

    navbar_toggler.click()
    time.sleep(1) 
    assert not navbar_content.is_displayed()