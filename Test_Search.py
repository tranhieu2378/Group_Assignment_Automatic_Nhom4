import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from function import Search_Form
from variable import SearchValid, SearchInValid, NoAccentSearch, symbolSearch1

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Testcase 1: Tìm kiếm sản phẩm thành công
def test_TK_001(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, SearchValid)
    assert driver.find_element(By.CLASS_NAME, "men-pro-item")


# Testcase 2: Tìm kiếm sản phẩm không tồn tại
def test_TK_002(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, SearchInValid)
    no_results_message = driver.find_element(By.XPATH, "//div[@class='ads-grid py-sm-5 py-4']//h5[@class='text-center text-dark']").text
    # Expected result
    assert "Không tìm thấy sản phẩm" in no_results_message

# Testcase 3: Tìm kiếm sản phẩm không ghi dấu
def test_TK_003(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, NoAccentSearch)
    assert driver.find_element(By.CLASS_NAME, "men-pro-item")


# Testcase 4: Tìm kiếm sản phẩm ký tự % (Có bug - ghi báo cáo)
def test_TK_004(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, symbolSearch1)
    no_results_message = driver.find_element(By.XPATH, "//div[@class='ads-grid py-sm-5 py-4']//h5[@class='text-center text-dark']").text
    assert "Không tìm thấy sản phẩm" in no_results_message

# Testcase 5: Tìm kiếm sản phẩm để trống (Có bug - ghi báo cáo)
def test_TK_005(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, "")
    assert driver.find_element(By.CLASS_NAME, "men-pro-item")


# Testcase 6: Tìm kiếm sản phẩm khi nhập lệnh Or sql (Có bug - ghi báo cáo)
def test_TK_006(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, "'Dưa lưới' Or 'Táo'")
    no_results_message = driver.find_element(By.XPATH, "//div[@class='ads-grid py-sm-5 py-4']//h5[@class='text-center text-dark']").text
    assert "Không tìm thấy sản phẩm" in no_results_message

# Testcase 7: Tìm kiếm sản phẩm khi nhập lệnh scrpit (Có bug - ghi báo cáo)
def test_TK_007(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    Search_Form(driver, "<script>alert('Lỗi đây nè')</script>")
    no_results_message = driver.find_element(By.XPATH, "//div[@class='ads-grid py-sm-5 py-4']//h5[@class='text-center text-dark']").text
    assert "Không tìm thấy sản phẩm" in no_results_message

# Testcase 8: Lọc sản phẩm theo danh mục
def test_TK_008(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    driver.find_element(By.NAME, "agileinfo_search").click()
    driver.find_element(By.XPATH, "//option[@value='1']").click()
    # Expected result
    title = driver.find_element(By.XPATH, "//h3[@class='tittle-w3l text-center mb-lg-5 mb-sm-4 mb-3']")
    assert "Trái cây nhập" in title.text


# Testcase 9: Sắp xếp sản phẩm theo giá
def test_TK_009(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    driver.find_element(By.NAME, "sort").click()
    driver.find_element(By.XPATH, "//option[@value='asc']").click()
    # Expected result
    prices_elements = driver.find_elements(By.CSS_SELECTOR, ".row .item_price")
    prices = []
    for price_element in prices_elements:
        price_text = price_element.text.replace(",", "").replace(".đ", "").strip()
        prices.append(int(price_text))
    
    assert prices == sorted(prices)