import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage

pytestmark = pytest.mark.ui


# TC_CT_01: Thêm 1 sản phẩm từ trang danh sách
def test_add_one_item(page, logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    expect(logged_in.cart_badge).to_have_text("1")
    expect(page.locator("[data-test='remove-sauce-labs-backpack']")).to_be_visible()


# TC_CT_02: Thêm nhiều sản phẩm
def test_add_three_items(logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")
    logged_in.add_to_cart("sauce-labs-bolt-t-shirt")
    expect(logged_in.cart_badge).to_have_text("3")


# TC_CT_03: Thêm toàn bộ 6 sản phẩm
def test_add_all_items(page, logged_in):
    add_buttons = page.locator("[data-test^='add-to-cart']")
    while add_buttons.count() > 0:
        add_buttons.first.click()
    expect(logged_in.cart_badge).to_have_text("6")


# TC_CT_05: Xóa hết sản phẩm thì icon giỏ không còn số
def test_badge_disappears_when_cart_empty(logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.remove_from_cart("sauce-labs-backpack")
    expect(logged_in.cart_badge).to_be_hidden()


# TC_CT_06: Thêm sản phẩm từ trang chi tiết
def test_add_item_from_detail_page(page, logged_in):
    page.get_by_text("Sauce Labs Backpack").click()
    page.locator("[data-test='add-to-cart']").click()
    expect(logged_in.cart_badge).to_have_text("1")

    page.locator("[data-test='back-to-products']").click()
    expect(page.locator("[data-test='remove-sauce-labs-backpack']")).to_be_visible()


# TC_CT_07: Giỏ hàng hiển thị đúng tên, giá, số lượng
def test_cart_shows_correct_item(page, logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.open_cart()

    cart = CartPage(page)
    expect(cart.items).to_have_count(1)
    expect(cart.item_names).to_have_text(["Sauce Labs Backpack"])
    expect(cart.item_prices).to_have_text(["$29.99"])
    expect(cart.item_quantities).to_have_text(["1"])


# TC_CT_08: Xóa sản phẩm trong trang giỏ hàng
def test_remove_item_in_cart_page(page, logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")
    logged_in.open_cart()

    cart = CartPage(page)
    cart.remove("sauce-labs-backpack")
    expect(cart.items).to_have_count(1)
    expect(logged_in.cart_badge).to_have_text("1")


# TC_CT_09: Continue Shopping giữ nguyên giỏ hàng
def test_continue_shopping_keeps_cart(page, logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.open_cart()

    CartPage(page).continue_shopping()
    logged_in.expect_loaded()
    expect(logged_in.cart_badge).to_have_text("1")


# TC_CT_10: Giỏ hàng giữ nguyên sau khi tải lại trang
def test_cart_kept_after_reload(page, logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")
    page.reload()
    expect(logged_in.cart_badge).to_have_text("2")


# TC_CT_11: Reset App State làm trống giỏ hàng
def test_reset_app_state_empties_cart(page, logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")

    page.locator("#react-burger-menu-btn").click()
    page.locator("#reset_sidebar_link").click()
    expect(logged_in.cart_badge).to_be_hidden()