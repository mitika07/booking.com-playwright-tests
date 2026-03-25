from playwright.sync_api import Page
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """
    Page Object for Booking.com search results page.
    Handles filtering, sorting, and reading results.
    """

    # --- Locators ---
    RESULTS_CONTAINER = '[data-testid="property-card"]'
    RESULT_TITLE_LINK = '[data-testid="title-link"]'
    RESULT_TITLES = '[data-testid="title"]'
    RESULT_PRICES = '[data-testid="price-and-discounted-price"]'
    SORT_DROPDOWN = '[data-testid="sorters-dropdown-trigger"]'
    FILTER_ENTIRE_HOMES = 'input[name="ht_id=220"]'
    STAR_FILTER = 'input[name="class={}"]'
    LOADING_INDICATOR = '[data-testid="skeleton-loader"]'
    RESULT_COUNT = '[data-testid="search-results-stats"]'
    # PRICE_LOW_TO_HIGH = '[data-id="price"]'
    # PRICE_HIGH_TO_LOW = '[data-id="price_from_high_to_low"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def wait_for_results(self):
        self.page.wait_for_selector(self.RESULTS_CONTAINER, timeout=30000)

    def get_result_count(self) -> int:
        cards = self.page.locator(self.RESULTS_CONTAINER)
        return cards.count()

    def get_all_hotel_names(self) -> list[str]:
        self.wait_for_results()
        titles = self.page.locator(self.RESULT_TITLES).all()
        return [t.inner_text() for t in titles]

    def get_all_prices(self) -> list[str]:
        prices = self.page.locator(self.RESULT_PRICES).all()
        return [p.inner_text() for p in prices]

    def sort_by(self, option: str):
        """
        Sort results.
        :param option: 'price' | 'review_score' | 'distance'
        """
        self.page.click(self.SORT_DROPDOWN)
        sort_option = option.capitalize()
        self.page.locator(f'[aria-label="{sort_option}"]').click()
        self.page.wait_for_load_state("domcontentloaded")

    def filter_by_stars(self, stars: int):
        locator = self.STAR_FILTER.format(stars)
        self.page.locator(locator).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_first_result(self):
        self.wait_for_results()
        # Wait for results to fully stabilise after initial render
        self.page.wait_for_timeout(2000)
        # Re-query fresh — DOM may have re-rendered after initial load
        title_link = self.page.locator(
            f'{self.RESULTS_CONTAINER} {self.RESULT_TITLE_LINK}'
        ).first
        title_link.wait_for(state="visible", timeout=10000)
        title_link.click()

    def results_are_displayed(self) -> bool:
        return self.get_result_count() > 0
