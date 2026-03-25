from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page Object for Booking.com homepage.
    Handles search form interactions.
    """

    URL = "https://www.booking.com"

    # --- Locators ---
    CALENDAR = '[data-testid="searchbox-datepicker-calendar"]'
    DESTINATION_INPUT = '[data-testid="destination-container"] input'
    CHECKIN_DATE = '[data-testid="date-display-field-start"]'
    CHECKOUT_DATE = '[data-testid="date-display-field-end"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    OCCUPANCY_CONFIG = '[data-testid="occupancy-config"]'
    ADULTS_INCREASE = '[data-testid="occupancy-popup"] [aria-label="Increase number of Adults"]'
    ADULTS_DECREASE = '[data-testid="occupancy-popup"] [aria-label="Decrease number of Adults"]'
    COOKIE_ACCEPT = '#onetrust-accept-btn-handler'
    SIGN_IN_DISCOUNT_POP_UP = '[aria-label="Window offering discounts of 10% or more when you sign in to Booking.com"]'
    DISMISS_SIGN_IN_POP_UP = '[aria-label="Dismiss sign-in info."]'

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.navigate(self.URL)
        self._dismiss_cookie_banner()

    def _dismiss_cookie_banner(self):
        try:
            self.page.click(self.COOKIE_ACCEPT, timeout=5000)
        except Exception:
            pass  # Cookie banner may not appear every time

    def search_destination(self, destination: str):
        # Click and wait for the input to be ready
        self.page.click(self.DESTINATION_INPUT)
        self.page.wait_for_timeout(500)

        # Clear field first, then type slowly character by character
        self.page.fill(self.DESTINATION_INPUT, "")
        self.page.type(self.DESTINATION_INPUT, destination, delay=100)

        # Wait for autocomplete dropdown to appear
        self.page.wait_for_selector('[data-testid="autocomplete-result"]', state="visible", timeout=8000)
        self.page.wait_for_timeout(500)  # Let the list fully stabilize

        # Click first result
        first_result = self.page.locator('[data-testid="autocomplete-result"]').first
        first_result.wait_for(state="visible", timeout=5000)
        first_result.click()

        # Wait for the field to confirm the selection before moving on
        self.page.wait_for_timeout(800)

    def _open_calendar(self):
        """Open the calendar and wait until it is visible."""
        # self.page.click(self.CHECKIN_DATE)
        self.page.locator('[data-date]').first.wait_for(state="visible", timeout=8000)

    def _calendar_is_open(self) -> bool:
        return self.page.locator('[data-date]').first.is_visible()

    def _click_date(self, date_str: str):
        next_button = '[aria-label="Next month"]'  # removed the broken parent selector

        for _ in range(6):
            cell = self.page.locator(f'[data-date="{date_str}"]').first

            if cell.count() > 0 and cell.is_visible():
                cell.scroll_into_view_if_needed()
                cell.click()
                return

            # Date not visible yet — go to next month
            self.page.locator(next_button).click()
            self.page.wait_for_timeout(500)

        raise Exception(f"Could not find date {date_str} after scrolling 6 months")

    def select_dates(self, checkin: str, checkout: str):
        self._open_calendar()
        self._click_date(checkin)

        self.page.wait_for_timeout(600)

        # If calendar closed after check-in, reopen via checkout field
        if not self._calendar_is_open():
            self.page.wait_for_timeout(1000)
            # self.page.wait_for_selector(self.CALENDAR, state="visible", timeout=8000)

        self._click_date(checkout)
        self.page.wait_for_timeout(400)

    def set_adults(self, count: int):
        self.page.click(self.OCCUPANCY_CONFIG)
        # Reset to 2 (default) then adjust
        for _ in range(5):
            try:
                self.page.click(self.ADULTS_DECREASE, timeout=1000)
            except Exception:
                break
        for _ in range(count - 1):
            self.page.click(self.ADULTS_INCREASE)

    def click_search(self):
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")

    def close_sign_in_pop_up(self):
        if self.page.is_visible(self.SIGN_IN_DISCOUNT_POP_UP):
            self.page.click(self.DISMISS_SIGN_IN_POP_UP)
        else:
            return True
