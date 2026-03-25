from playwright.sync_api import Page
from pages.base_page import BasePage


class HotelPage(BasePage):
    """
    Page Object for an individual hotel details page on Booking.com.
    """

    # --- Locators ---
    HOTEL_NAME = '[id="hp_hotel_name"]'
    REVIEW_SCORE = '[data-testid="review-score-right-component"]'
    RESERVE_BUTTON = '[id="hp_book_now_button"]'
    ROOM_OPTIONS = '[id="available_rooms"]'
    MAP_SECTION = '#hotel_main_content'
    FACILITIES_SECTION = '[data-testid="PropertyDetails"]'
    PHOTOS_GALLERY = '[data-testid="bh-photo-slider"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def get_hotel_name(self) -> str:
        self.page.wait_for_selector(self.HOTEL_NAME)
        return self.page.locator(self.HOTEL_NAME).inner_text()

    def get_review_score(self) -> str:
        return self.page.locator(self.REVIEW_SCORE).inner_text()

    def is_reserve_button_visible(self) -> bool:
        return self.is_visible(self.RESERVE_BUTTON)

    def are_rooms_displayed(self) -> bool:
        return self.is_visible(self.ROOM_OPTIONS)

    def click_reserve(self):
        self.page.click(self.RESERVE_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")

    def get_room_count(self) -> int:
        rooms = self.page.locator(self.ROOM_OPTIONS)
        return rooms.count()
