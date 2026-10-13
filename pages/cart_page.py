from playwright.sync_api import Page


class CartPage:
    """Page Object cho màn hình giỏ hàng (Your Cart)."""

    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator(".cart_item")
        self.item_names = page.locator(".cart_item .inventory_item_name")
        self.item_prices = page.locator(".cart_item .inventory_item_price")
        self.item_quantities = page.locator(".cart_item .cart_quantity")
        self.continue_button = page.locator("[data-test='continue-shopping']")

    def remove(self, product_slug: str):
        self.page.locator(f"[data-test='remove-{product_slug}']").click()

    def continue_shopping(self):
        self.continue_button.click()