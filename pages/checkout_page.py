from playwright.sync_api import Page, expect


class CheckoutPage:
    """Page Object cho giỏ hàng và các bước thanh toán."""

    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.locator("[data-test='checkout']")
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.error_message = page.locator("[data-test='error']")
        self.item_prices = page.locator("[data-test='inventory-item-price']")
        self.subtotal = page.locator("[data-test='subtotal-label']")
        self.tax = page.locator("[data-test='tax-label']")
        self.total = page.locator("[data-test='total-label']")
        self.complete_header = page.locator("[data-test='complete-header']")

    def start_checkout(self):
        self.checkout_button.click()

    def fill_info(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    @staticmethod
    def _money(text: str) -> float:
        # "Item total: $39.98" -> 39.98
        return float(text.split("$")[-1])

    def get_item_prices(self) -> list[float]:
        return [self._money(t) for t in self.item_prices.all_inner_texts()]

    def get_summary(self) -> dict:
        return {
            "subtotal": self._money(self.subtotal.inner_text()),
            "tax": self._money(self.tax.inner_text()),
            "total": self._money(self.total.inner_text()),
        }

    def finish(self):
        self.finish_button.click()

    def expect_complete(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")
