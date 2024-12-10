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
from function import clear_field, link_detail, get_product_price, get_quantity_in_cart, get_total_price, addToCart_002, search_and_add_product, navigate_to_cart, calculate_total_in_cart, get_displayed_payment_total
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
    # Chuyển tới giỏ hàng
    navigate_to_cart(driver)
    # Tính tổng tiền từ các dòng sản phẩm
    calculated_total = calculate_total_in_cart(driver)
    # Lấy tổng tiền thanh toán hiển thị
    displayed_payment_total = get_displayed_payment_total(driver)

    # Kiểm tra tổng tiền
    assert calculated_total == displayed_payment_total, "Tổng tiền trong giỏ hàng không khớp!"


# Testcase 4: Xoá sản phẩm khỏi giỏ hàng
def test_DEL_CART_001(driver):
    # driver.get("http://localhost/ASM_PHP1/index.php")
    test_TGH_001(driver)
    driver.find_element(By.CLASS_NAME, "w3view-cart").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//td[@class='invert col_action']/a"))
    )
    driver.find_element(By.XPATH, "//td[@class='invert col_action']/a").click()
    
    WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()

    # Expected result
    assert "Xóa thành công" in alert_text

    
# Testcase 5: Xoá hết tất cả sản phẩm
def test_DEL_CART_002(driver):
    # 
    # driver.get("http://localhost/ASM_PHP1/index.php")
    test_TGH_003(driver)
    driver.find_element(By.CLASS_NAME, "w3view-cart").click()

    try:

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//tbody[@class='scrollable-body']/tr"))
        )
        
        delete_buttons = driver.find_elements(By.XPATH, "//tbody[@class='scrollable-body']//a[text()='Xóa']")

        while delete_buttons:
            delete_buttons[0].click() 

            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()

            assert "Xóa thành công" in alert_text, f"Expected 'Xóa thành công' but got {alert_text}"

            WebDriverWait(driver, 10).until(EC.staleness_of(delete_buttons[0]))
            delete_buttons = driver.find_elements(By.XPATH, "//tbody[@class='scrollable-body']//a[text()='Xóa']")

    except TimeoutException:
        print("No products to delete; checking for empty cart message.")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//td[text()='Chưa có sản phẩm']"))
    )
    message = driver.find_element(By.XPATH, "//td[text()='Chưa có sản phẩm']")

    assert message.is_displayed(), "Expected 'Chưa có sản phẩm' message to be displayed."


# Testcase 6: Cập nhật một sản phẩm trong giỏ hàng
def test_UPDATE_CART_001(driver):
    # 
    test_TGH_001(driver)
    # driver.find_element(By.CLASS_NAME, "w3view-cart").click()
    time.sleep(2)

    random_number = random.randint(2, 10)
    # Tìm ô input số lượng và điền số ngẫu nhiên
    quantity_input = driver.find_element(By.NAME, "soluong[]")
    quantity_input.clear()  # Xóa giá trị hiện tại
    quantity_input.send_keys(str(random_number))
    time.sleep(2)

    driver.find_element(By.NAME, "capnhatsoluong").click()
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    time.sleep(2)

     # Tìm phần tử số lượng
    quantity_element = driver.find_element(By.CSS_SELECTOR, "td.col_soluong input[type='number']")
    quantity = int(quantity_element.get_attribute("value"))  # Lấy giá trị số lượng
    # Tìm phần tử giá sản phẩm
    price_element = driver.find_element(By.CSS_SELECTOR, "td.col_gia")
    price_text = price_element.text.strip()  # Lấy giá dạng chuỗi
    price = int(price_text.replace(",", "").replace("đ", ""))  # Chuyển đổi thành số nguyên
    # Tìm phần tử tổng tiền
    total_element = driver.find_element(By.CSS_SELECTOR, "td.col_tongtien")
    total_text = total_element.text.strip()  # Lấy tổng tiền dạng chuỗi
    total = int(total_text.replace(",", "").replace("đ", ""))  # Chuyển đổi thành số nguyên

    # Kiểm tra tổng tiền = giá * số lượng
    assert total == price * quantity
    assert "Cập nhật giỏ hàng thành công" in alert_text


# Testcase 7: Cập nhật nhiều sản phẩm trong giỏ hàng
def test_UPDATE_CART_002(driver):
    # Gọi testcase thêm sản phẩm vào giỏ hàng trước khi cập nhật
    test_TGH_003(driver)

    time.sleep(2)

    # Lấy tất cả các dòng sản phẩm trong giỏ hàng
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.scrollable-body tr.rem1")

    # Cập nhật số lượng ngẫu nhiên cho từng sản phẩm
    for row in rows:
        quantity_input = row.find_element(By.NAME, "soluong[]")
        quantity_input.clear()
        
        random_number = random.randint(2, 10)  # Số lượng mới ngẫu nhiên
        quantity_input.send_keys(str(random_number))

    # Nhấn nút cập nhật giỏ hàng
    driver.find_element(By.NAME, "capnhatsoluong").click()
    time.sleep(2)

    # Chờ thông báo alert xuất hiện
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.scrollable-body tr.rem1")
    # Duyệt qua từng dòng để tính tổng tiền
    calculated_total = 0
    for row in rows:
        # Lấy giá trị tổng tiền từng sản phẩm
        total_text = row.find_element(By.CSS_SELECTOR, "td.col_tongtien").text.strip()
        total = int(total_text.replace(",", "").replace("đ", ""))  # Chuyển đổi chuỗi thành số nguyên
        
        # Cộng tổng tiền của sản phẩm vào tổng tiền đã tính
        calculated_total += total

    # Lấy tổng tiền thanh toán từ giao diện
    payment_total_text = driver.find_element(By.CSS_SELECTOR, "td.col_tongthanhtoan span").text.strip()
    displayed_payment_total = int(payment_total_text.replace(",", "").replace("đ", ""))

    # Kiểm tra tổng tiền đã tính có khớp với tổng tiền thanh toán hiển thị không
    assert calculated_total == displayed_payment_total

    # Kiểm tra thông báo thành công
    assert "Cập nhật giỏ hàng thành công" in alert_text

