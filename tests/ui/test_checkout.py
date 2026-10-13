import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

BASE = "https://www.saucedemo.com"


# ---------- Precondition dùng riêng cho file này ----------

@pytest.fixture
def on_info_page(page, logged_in, checkout):
    """Đã thêm Backpack vào giỏ và đang ở bước nhập thông tin."""
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.open_cart()
    checkout.start_checkout()
    return checkout


@pytest.fixture
def on_overview_page(page, logged_in, checkout):
    """Đã thêm Backpack + Bolt T-Shirt, nhập thông tin hợp lệ, đang ở trang Overview."""
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bolt-t-shirt")
    logged_in.open_cart()
    checkout.start_checkout()
    checkout.fill_info("Thuy", "Ta", "100000")
    return checkout


# ---------- Test case ----------

# TC_CO_02: Bấm Checkout chuyển sang bước nhập thông tin
def test_checkout_opens_information_page(page, on_info_page):
    expect(page).to_have_url(f"{BASE}/checkout-step-one.html")
    expect(page.locator("[data-test='title']")).to_have_text("Checkout: Your Information")


# TC_CO_03, TC_CO_04, TC_CO_06: Bỏ trống ô bắt buộc
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Ta", "100000", "First Name is required"),   # TC_CO_03
        ("Thuy", "", "100000", "Last Name is required"),  # TC_CO_04
        ("", "", "", "First Name is required"),           # TC_CO_06
    ],
    ids=["empty_first_name", "empty_last_name", "all_empty"],
)
def test_checkout_required_fields(page, on_info_page, first, last, postal, expected_error):
    on_info_page.fill_info(first, last, postal)
    expect(on_info_page.error_message).to_contain_text(expected_error)
    expect(page).to_have_url(f"{BASE}/checkout-step-one.html")


# TC_CO_09: Trang Overview hiển thị đúng sản phẩm
def test_overview_shows_correct_items(page, on_overview_page):
    names = page.locator(".cart_item .inventory_item_name")
    expect(names).to_have_text(["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"])
    expect(page.locator(".cart_item .cart_quantity")).to_have_text(["1", "1"])


# TC_CO_11: Tax bằng 8% Item total
def test_tax_is_8_percent(on_overview_page):
    summary = on_overview_page.get_summary()
    assert summary["tax"] == pytest.approx(round(summary["subtotal"] * 0.08, 2))


# TC_CO_13: Cancel ở bước nhập thông tin quay về giỏ hàng
def test_cancel_on_information_page(page, on_info_page):
    page.locator("[data-test='cancel']").click()
    expect(page).to_have_url(f"{BASE}/cart.html")
    expect(page.locator(".cart_item")).to_have_count(1)


# TC_CO_14: Cancel ở bước Overview quay về trang sản phẩm
def test_cancel_on_overview_page(page, logged_in, on_overview_page):
    page.locator("[data-test='cancel']").click()
    logged_in.expect_loaded()
    expect(logged_in.cart_badge).to_have_text("2")


# TC_CO_15: Back Home sau khi đặt hàng, giỏ hàng trống
def test_back_home_after_order(page, logged_in, on_overview_page):
    on_overview_page.finish()
    on_overview_page.expect_complete()

    page.locator("[data-test='back-to-products']").click()
    logged_in.expect_loaded()
    expect(logged_in.cart_badge).to_be_hidden()