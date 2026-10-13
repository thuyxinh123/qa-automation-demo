import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.ui


# TC_LG_01: Đăng nhập thành công
def test_login_success(page, login_page):
    login_page.login("standard_user", "secret_sauce")
    InventoryPage(page).expect_loaded()


# TC_LG_02: Đăng nhập bằng phím Enter
def test_login_with_enter_key(page, login_page):
    login_page.username.fill("standard_user")
    login_page.password.fill("secret_sauce")
    login_page.password.press("Enter")
    InventoryPage(page).expect_loaded()


# TC_LG_03: Mật khẩu hiển thị dạng ẩn
def test_password_is_masked(login_page):
    expect(login_page.password).to_have_attribute("type", "password")


# Các case đăng nhập lỗi: cùng các bước, chỉ khác dữ liệu
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("", "", "Username is required"),                                   # TC_LG_04
        ("", "secret_sauce", "Username is required"),                       # TC_LG_05
        ("standard_user", "", "Password is required"),                      # TC_LG_06
        ("standard_user", "wrong_password", "Username and password do not match"),  # TC_LG_07
        ("abc_user", "secret_sauce", "Username and password do not match"),         # TC_LG_08
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),# TC_LG_09
        ("Standard_User", "secret_sauce", "Username and password do not match"),    # TC_LG_10
    ],
    ids=[
        "both_empty",
        "empty_username",
        "empty_password",
        "wrong_password",
        "user_not_exist",
        "locked_user",
        "wrong_case_username",
    ],
)
def test_login_negative(login_page, username, password, expected_error):
    login_page.login(username, password)
    login_page.expect_error(expected_error)


# TC_LG_12: Vào thẳng trang sản phẩm khi chưa đăng nhập
def test_open_inventory_without_login(page, login_page):
    page.goto("https://www.saucedemo.com/inventory.html")
    login_page.expect_error("You can only access '/inventory.html' when you are logged in")


# TC_LG_13: Bấm nút X để đóng thông báo lỗi
def test_close_error_message(page, login_page):
    login_page.login("", "")
    page.locator(".error-button").click()
    expect(login_page.error_message).to_be_hidden()


# TC_LG_14: Đăng xuất
def test_logout(page, logged_in):
    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("[data-test='login-button']")).to_be_visible()