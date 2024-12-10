import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from variable import emailValid, passwordValid
import random
# @pytest.fixture
# def driver():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     yield driver
#     driver.quit()

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()  # Thêm trình duyệt Firefox
    else:
        raise ValueError("Unsupported browser")
    
    driver.maximize_window()
    yield driver
    driver.quit()
    
# -------------------------------------------- Modal --------------------------------------------
# Mở modal đăng nhập
def open_login_modal(driver):
    driver.get('http://localhost/ASM_PHP1/index.php')
    driver.find_element(By.CSS_SELECTOR, "li.text-center.border-right.text-white > a[data-target='#loginModal']").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginModal"))
    )

# Mở modal đăng ký
def open_register_modal(driver):
    driver.get('http://localhost/ASM_PHP1/index.php')
    driver.find_element(By.CSS_SELECTOR, "li.text-center.text-white > a[data-target='#registerModal']").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "registerModal"))
    )


# -------------------------------------------- Alert --------------------------------------------
# Hàm alert Ok và lấy alertText
def handle_alert(driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.alert_is_present()
    )
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    return alert_text

# Message input
def handle_message_input(driver, fieldInput):
    field = driver.find_element(By.NAME, fieldInput)
    validation_message = driver.execute_script("return arguments[0].validationMessage;", field)
    return  validation_message

# -------------------------------------------- Nhập Form --------------------------------------------
# Nhập form đăng nhập
def Login_Form(driver, emailValid, passwordValid):
    driver.find_element(By.NAME, "email_login").send_keys(emailValid)
    driver.find_element(By.NAME, "password_login").send_keys(passwordValid)

# Nhập form đăng ký
def Register_Form(driver, name, email, phone, address, password):
    driver.find_element(By.NAME, "register_name").send_keys(name)
    driver.find_element(By.NAME, "register_email").send_keys(email)
    driver.find_element(By.NAME, "register_phone").send_keys(phone)
    driver.find_element(By.NAME, "register_address").send_keys(address)
    driver.find_element(By.NAME, "register_password").send_keys(password)

# Nhập form tư vấn
def Contact_Form(driver, contactName, contactEmail, contactMessage):
    driver.find_element(By.NAME, "Name").send_keys(contactName)
    driver.find_element(By.NAME, "Email").send_keys(contactEmail)
    driver.find_element(By.NAME, "Message").send_keys(contactMessage)

# Form đổi thông tin
def Update_Profile_Form(driver, nameProf, addressProf, phoneProf):
    driver.find_element(By.NAME, "name_user").send_keys(nameProf)
    driver.find_element(By.NAME, "address_user").send_keys(addressProf)
    driver.find_element(By.NAME, "phone_user").send_keys(phoneProf)

# So sánh giá trị sau khi cập nhật
def verify_updated_information(driver, expected_name, expected_address, expected_phone):
    # driver.refresh()  # Tải lại trang
    driver.get("http://localhost/ASM_PHP1/index.php?quanli=suathongtin")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "name_user"))
    )
    
    # Lấy giá trị hiện tại trong các trường
    actual_name = driver.find_element(By.NAME, "name_user").get_attribute("value")
    actual_address = driver.find_element(By.NAME, "address_user").get_attribute("value")
    actual_phone = driver.find_element(By.NAME, "phone_user").get_attribute("value")
    
    # So sánh giá trị
    assert actual_name == expected_name
    assert actual_address == expected_address
    assert actual_phone == expected_phone

# Form đổi mật khẩu
def Update_Password_Form(driver, oldPwd, newPwd1, newPwd2):
    driver.find_element(By.NAME, "matkhaucu").send_keys(oldPwd)
    driver.find_element(By.NAME, "matkhaumoi_1").send_keys(newPwd1)
    driver.find_element(By.NAME, "matkhaumoi_2").send_keys(newPwd2)

# Form tìm kiếm
def Search_Form(driver, keyword):
    driver.find_element(By.CLASS_NAME, "seach_product").send_keys(keyword)
    driver.find_element(By.CLASS_NAME, "seach_btn").click()

# -------------------------------------------- Login --------------------------------------------
# Đăng nhập 1
def DN_001(driver):
    # Steps
    open_login_modal(driver)
    Login_Form(driver, emailValid, passwordValid)
    driver.find_element(By.NAME, "login_home").click()
    handle_alert(driver)


# Đăng nhập 2
def DN_002(driver, email, password):
    # Steps
    open_login_modal(driver)
    driver.find_element(By.NAME, "email_login").send_keys(email)
    driver.find_element(By.NAME, "password_login").send_keys(password)
    driver.find_element(By.NAME, "login_home").click()
    handle_alert(driver)


# -------------------------------------------- Chi tiết sản phẩm --------------------------------------------
# Chi tiết sp
def link_detail(driver):
    men_cart_pro = driver.find_element(By.CLASS_NAME, "men-cart-pro") 
    actions = ActionChains(driver) 
    actions.move_to_element(men_cart_pro).perform() 

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "link-product-add-cart"))
    )
    driver.find_element(By.CLASS_NAME, "link-product-add-cart") .click()


# -------------------------------------------- Clear Form --------------------------------------------
# Clear form
def clear_field(element):
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.BACKSPACE)


# -------------------------------------------- Điều hướng --------------------------------------------
# Điều hướng đến trang quản lý người dùng
def navigate_qlnd(driver):
    user_dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "userDropdown"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(user_dropdown).perform()

    profile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='?quanli=userinfor']"))
    )
    profile_button.click()

# Điều hướng đến trang liên hệ
def navigate_contact(driver):
    # Step 1: Truy cập trang chủ
    driver.get("http://localhost/ASM_PHP1/index.php")
    # Step 2: Đi đến trang liên hệ
    driver.find_element(By.XPATH, "//a[@href='?quanli=lienhe']").click()

# -------------------------------------------- Tìm kiếm --------------------------------------------
# Tìm kiếm một sản phẩm


# -------------------------------------------- Giỏ hàng --------------------------------------------
# Thêm một sản phẩm nhiều số lượng vào giỏ hàng
def addToCart_002(driver):
    link_detail(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "soluong"))
    )
    number = random.randint(1, 20)
    soluong = driver.find_element(By.NAME, "soluong")
    clear_field(soluong)
    soluong.send_keys(str(number))

# Lấy giá sản phẩm
def get_product_price(driver):
    price_element = driver.find_element(By.CSS_SELECTOR, "td.col_gia")
    price_text = price_element.text.strip()
    return int(price_text.replace(",", "").replace("đ", ""))

# Lấy số lượng sản phẩm trong giỏ hàng
def get_quantity_in_cart(driver):
    quantity_element = driver.find_element(By.CSS_SELECTOR, "td.col_soluong input[type='number']")
    return int(quantity_element.get_attribute("value"))

# Lấy tổng tiền của sản phẩm
def get_total_price(driver):
    total_element = driver.find_element(By.CSS_SELECTOR, "td.col_tongtien")
    total_text = total_element.text.strip()
    return int(total_text.replace(",", "").replace("đ", ""))

# Nhập số lượng sản phẩm ngẫu nhiên
def set_quantity(driver, min_value=1, max_value=20):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "soluong"))
    )
    number = random.randint(min_value, max_value)
    soluong = driver.find_element(By.NAME, "soluong")
    clear_field(soluong)
    soluong.send_keys(str(number))
    return number

# Thêm sản phẩm vào giỏ hàng
def add_to_cart(driver):
    driver.find_element(By.NAME, "themgiohang").click()

# Tìm kiếm và thêm sản phẩm vào giỏ hàng
def search_and_add_product(driver, product):
    search_box = driver.find_element(By.CLASS_NAME, "seach_product")
    search_box.clear()
    search_box.send_keys(product)
    driver.find_element(By.CLASS_NAME, "seach_btn").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "men-pro-item"))
    )
    link_detail(driver)

    set_quantity(driver)
    add_to_cart(driver)

    driver.find_element(By.XPATH, "//a[@href='index.php']").click()


# Chuyển tới giỏ hàng
def navigate_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "w3view-cart").click()

# Tính tổng tiền các sản phẩm trong giỏ hàng
def calculate_total_in_cart(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody.scrollable-body tr.rem1")
    calculated_total = 0
    for row in rows:
        calculated_total += get_total_price(row)
    return calculated_total

# Lấy tổng tiền thanh toán từ giao diện
def get_displayed_payment_total(driver):
    payment_total_text = driver.find_element(By.CSS_SELECTOR, "td.col_tongthanhtoan span").text.strip()
    return int(payment_total_text.replace(",", "").replace("đ", ""))