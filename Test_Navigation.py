import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Điều hướng đến trang thông tin cá nhân khi chưa đăng nhập
def test_DH_001(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    driver.find_element(By.CLASS_NAME, "dropdown").find_element(By.CLASS_NAME, "w3view-cart").click()

    WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )
    alert = driver.switch_to.alert

    assert "Vui lòng đăng nhập trước khi sử dụng chức năng này" in alert.text


# Điều hướng đến trang danh mục sản phẩm
def test_DH_002(driver):
    # Steps
    driver.get("http://localhost/ASM_PHP1/index.php")
    category_link = driver.find_element(By.XPATH, "//li[@class='nav-item mr-lg-2 mb-lg-0 mb-2']/a[@href='?quanli=danhmuc&id=1']")
    category_link.click()

    # Expected result
    title_text = driver.find_element(By.CLASS_NAME, "tittle-w3l")
    assert "Trái cây nhập" in title_text.text


# Điều hướng đến trang đơn mua khi chưa đăng nhập
def test_DH_003(driver):
    # Steps
    driver.get("http://localhost/ASM_PHP1/index.php")
    category_link = driver.find_element(By.XPATH, "//li[@class='text-center border-right text-white']/a[@href='index.php?quanli=dondamua']")
    category_link.click()

    # Expected result
    title_text = driver.find_element(By.XPATH, "//h5[@class='text-center mt-5']")
    assert "Vui lòng đăng nhập để sử dụng chức năng này" in title_text.text

# Điều hướng đến trang thanh toán khi chưa đăng nhập
def test_DH_004(driver):
    driver.get("http://localhost/ASM_PHP1/index.php?quanli=thanhtoan")
    time.sleep(2)
    # Expected result
    assert "http://localhost/ASM_PHP1/index.php" == driver.current_url


# Điều hướng đến trang thông tin cá nhân bằng url khi chưa đăng nhập
def test_DH_005(driver):
    driver.get("http://localhost/ASM_PHP1/index.php?quanli=userinfor")
    time.sleep(2)
    # Expected result
    assert "http://localhost/ASM_PHP1/index.php" == driver.current_url

# Điều hướng đến trang chi tiết 1 sản phẩm id rỗng
def test_DH_006(driver):
    driver.get("http://localhost/ASM_PHP1/index.php?quanli=chitietsp&id=")
    time.sleep(2)
    # Expected result
    assert "http://localhost/ASM_PHP1/index.php" == driver.current_url

# Điều hướng đến trang đơn mua hàng của một tài khoản khác khi không cần đăng nhập
def test_DH_007(driver):
    driver.get("http://localhost/ASM_PHP1/index.php?quanli=chitietdonmua&madonhang=4613")
    time.sleep(2)
    # Expected result
    assert "http://localhost/ASM_PHP1/index.php" == driver.current_url