import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random
from function import clear_field, link_detail, get_product_price, get_quantity_in_cart, get_total_price, addToCart_002, search_and_add_product, navigate_to_cart, calculate_total_in_cart, get_displayed_payment_total, handle_alert
from variable import lst_prod

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Testcase 1: Kiểm tra thêm 1 sản phẩm vào giỏ hàng
def test_TGH_001(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    driver.find_element(By.NAME, "themgiohang").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//tbody[@class='scrollable-body']/tr"))
    )
    # Expected result
    assert "http://localhost/ASM_PHP1/index.php?quanli=giohang" in driver.current_url
    assert driver.find_element(By.XPATH, "//tbody[@class='scrollable-body']/tr")


# Testcase 2: Kiểm tra thêm một sản phẩm với số lượng nhiều
def test_TGH_002(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    # Thêm SP nhiều sl 
    addToCart_002(driver)
    driver.find_element(By.NAME, "themgiohang").click()
    quantity = get_quantity_in_cart(driver)
    price = get_product_price(driver)
    total = get_total_price(driver)
    # Expected result
    assert total == price * quantity

# Testcase 3: Kiểm tra thêm nhiều sản phẩm, nhiều số lượng
def test_TGH_003(driver):
    driver.get("http://localhost/ASM_PHP1/index.php")
    # Chọn ngẫu nhiên 5 sản phẩm
    random_products = random.sample(lst_prod, 5)
    for product in random_products:
        search_and_add_product(driver, product)

    navigate_to_cart(driver)

    calculated_total = calculate_total_in_cart(driver)
    displayed_payment_total = get_displayed_payment_total(driver)
    # Expected result
    assert calculated_total == displayed_payment_total


# Testcase 4: Xoá sản phẩm khỏi giỏ hàng
def test_DEL_CART_001(driver):
    test_TGH_001(driver)
    driver.find_element(By.CLASS_NAME, "w3view-cart").click()
    driver.find_element(By.XPATH, "//td[@class='invert col_action']/a").click()   
    alert_text = handle_alert(driver)
    # Expected result
    assert "Xóa thành công" in alert_text

    
# Testcase 5: Xoá hết tất cả sản phẩm
def test_DEL_CART_002(driver):
    # Thêm nhiều sp vào gh
    test_TGH_003(driver)
    driver.find_element(By.CLASS_NAME, "w3view-cart").click()
    
    delete_buttons = driver.find_elements(By.XPATH, "//tbody[@class='scrollable-body']//a[text()='Xóa']")

    while delete_buttons:
        delete_buttons[0].click() 
        alert_text = handle_alert(driver)
        assert "Xóa thành công" in alert_text
        WebDriverWait(driver, 10).until(EC.staleness_of(delete_buttons[0]))
        delete_buttons = driver.find_elements(By.XPATH, "//tbody[@class='scrollable-body']//a[text()='Xóa']")

    message = driver.find_element(By.XPATH, "//td[text()='Chưa có sản phẩm']")
    assert message.is_displayed()



# Testcase 6: Cập nhật một sản phẩm trong giỏ hàng
def test_UPDATE_CART_001(driver):
    test_TGH_001(driver)

    random_number = random.randint(2, 10)
    quantity_input = driver.find_element(By.NAME, "soluong[]")
    clear_field(quantity_input)
    quantity_input.send_keys(str(random_number))

    driver.find_element(By.NAME, "capnhatsoluong").click()
    alert_text = handle_alert(driver)

    quantity = get_quantity_in_cart(driver)
    price = get_product_price(driver)
    total = get_total_price(driver)

    # Expected result
    assert total == price * quantity
    assert "Cập nhật giỏ hàng thành công" in alert_text


# Testcase 7: Cập nhật nhiều sản phẩm trong giỏ hàng
def test_UPDATE_CART_002(driver):
    test_TGH_003(driver)

    # Lấy tất cả các dòng sản phẩm trong giỏ hàng
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.scrollable-body tr.rem1")

    for row in rows:
        quantity_input = row.find_element(By.NAME, "soluong[]")
        quantity_input.clear()
        
        random_number = random.randint(2, 10)  
        quantity_input.send_keys(str(random_number))

    # Nhấn nút cập nhật giỏ hàng
    driver.find_element(By.NAME, "capnhatsoluong").click()
    alert_text = handle_alert(driver)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.scrollable-body tr.rem1")
    calculated_total = 0
    for row in rows:
        total_text = row.find_element(By.CSS_SELECTOR, "td.col_tongtien").text.strip()
        total = int(total_text.replace(",", "").replace("đ", ""))
        
        calculated_total += total

    # Lấy tổng tiền thanh toán từ giao diện
    displayed_payment_total = get_displayed_payment_total(driver)

    # So sánh tổng tiền đã tính và thanh toán
    assert calculated_total == displayed_payment_total
    assert "Cập nhật giỏ hàng thành công" in alert_text

