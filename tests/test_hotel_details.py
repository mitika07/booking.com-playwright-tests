import json
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.hotel_page import HotelPage


with open("test_data/search_data.json") as f:
    TEST_DATA = json.load(f)


class TestHotelDetails:
    """
    Tests covering the individual hotel details page.
    """

    def _navigate_to_first_result(self, page):
        """Helper: search and click on first hotel result."""
        search = TEST_DATA["valid_searches"][0]
        home = HomePage(page)
        home.open()
        home.search_destination(search["destination"])
        home.select_dates(search["checkin"], search["checkout"])
        home.click_search()

        results = SearchResultsPage(page)
        results.wait_for_results()

        # Wait for the new tab to open
        with page.context.expect_page() as new_page_info:
            results.click_first_result()

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")

        return HotelPage(new_page)

    def test_hotel_name_is_displayed(self, page):
        """Verify hotel name appears on the details page."""
        hotel = self._navigate_to_first_result(page)
        name = hotel.get_hotel_name()
        assert name.strip() != "", "Hotel name should not be empty"

    def test_reserve_button_is_visible(self, page):
        """Verify the Reserve button is present on hotel page."""
        hotel = self._navigate_to_first_result(page)
        assert hotel.is_reserve_button_visible(), "Reserve button not visible"

    def test_rooms_are_displayed(self, page):
        """Verify room options are shown on hotel page."""
        hotel = self._navigate_to_first_result(page)
        assert hotel.are_rooms_displayed(), "No room options displayed"
