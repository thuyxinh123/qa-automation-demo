from playwright.sync_api import Page, expect


class InventoryPage:
    """Page Object cho màn hình danh sách sản phẩm."""

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.items = page.locator("[data-test='inventory-item']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.sort_select = page.locator("[data-test='product-sort-container']")
        self.prices = page.locator("[data-test='inventory-item-price']")

    def expect_loaded(self):
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(self.title).to_have_text("Products")

    def add_to_cart(self, product_slug: str):
        # product_slug ví dụ: "sauce-labs-backpack"
        self.page.locator(f"[data-test='add-to-cart-{product_slug}']").click()

    def remove_from_cart(self, product_slug: str):
        self.page.locator(f"[data-test='remove-{product_slug}']").click()

    def sort_by(self, value: str):
        # value: "az", "za", "lohi", "hilo"
        self.sort_select.select_option(value)

    def get_prices(self) -> list[float]:
        return [float(t.replace("$", "")) for t in self.prices.all_inner_texts()]

    def open_cart(self):
        self.cart_link.click()
