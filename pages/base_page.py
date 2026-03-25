from playwright.sync_api import Page


class BasePage:
    """
    Base class for all page objects.
    Contains shared/reusable methods across pages.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        self.page.wait_for_selector(selector, timeout=timeout)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def take_screenshot(self, name: str):
        self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
