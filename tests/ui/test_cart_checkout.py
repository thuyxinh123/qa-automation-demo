import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_add_and_remove_item_updates_badge(logged_in):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")
    expect(logged_in.cart_badge).to_have_text("2")

    logged_in.remove_from_cart("sauce-labs-backpack")
    expect(logged_in.cart_badge).to_have_text("1")


def test_sort_price_low_to_high(logged_in):
    logged_in.sort_by("lohi")
    prices = logged_in.get_prices()
    assert prices == sorted(prices)


def test_checkout_total_is_correct(logged_in, checkout):
    """Kiểm tra tính đúng của số tiền: subtotal = tổng giá, total = subtotal + tax."""
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bolt-t-shirt")
    logged_in.open_cart()

    checkout.start_checkout()
    checkout.fill_info("Thuy", "Ta", "100000")

    item_prices = checkout.get_item_prices()
    summary = checkout.get_summary()

    assert summary["subtotal"] == pytest.approx(sum(item_prices))
    assert summary["total"] == pytest.approx(summary["subtotal"] + summary["tax"], abs=0.01)

    checkout.finish()
    checkout.expect_complete()


def test_checkout_requires_postal_code(logged_in, checkout):
    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.open_cart()

    checkout.start_checkout()
    checkout.fill_info("Thuy", "Ta", "")
    expect(checkout.error_message).to_contain_text("Postal Code is required")


def test_sort_name_z_to_a(logged_in):
    logged_in.sort_by("za")
    names = logged_in.page.locator("[data-test='inventory-item-name']").all_inner_texts()
    assert names == sorted(names, reverse=True)