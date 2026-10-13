import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def logged_in(page, login_page):
    """Đăng nhập sẵn bằng standard_user, trả về InventoryPage."""
    login_page.login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(page)
    inventory.expect_loaded()
    return inventory


@pytest.fixture
def checkout(page):
    return CheckoutPage(page)
