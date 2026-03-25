import json
import time
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


# Load test data
with open("test_data/search_data.json") as f:
    TEST_DATA = json.load(f)


class TestSearch:
    """
    Tests covering the core search functionality on Booking.com.
    """

    def test_homepage_loads(self, page):
        """Verify Booking.com homepage loads successfully."""
        home = HomePage(page)
        home.open()
        assert "Booking.com" in home.get_title()

    def test_search_returns_results(self, page):
        """Search for a destination and verify results are displayed."""
        home = HomePage(page)
        home.open()

        # home.close_sign_in_pop_up()
        search = TEST_DATA["valid_searches"][0]
        home.search_destination(search["destination"])
        home.select_dates(search["checkin"], search["checkout"])
        home.click_search()

        results = SearchResultsPage(page)
        results.wait_for_results()

        assert results.results_are_displayed(), "No results found for valid search"

    def test_search_shows_multiple_results(self, page):
        """Verify that search returns more than one property."""
        home = HomePage(page)
        home.open()

        search = TEST_DATA["valid_searches"][0]
        home.search_destination(search["destination"])
        home.select_dates(search["checkin"], search["checkout"])
        home.click_search()

        results = SearchResultsPage(page)
        results.wait_for_results()

        count = results.get_result_count()
        assert count > 1, f"Expected multiple results but got {count}"

    def test_search_result_names_not_empty(self, page):
        """Verify hotel names are populated in results."""
        home = HomePage(page)
        home.open()

        search = TEST_DATA["valid_searches"][0]
        home.search_destination(search["destination"])
        home.select_dates(search["checkin"], search["checkout"])
        home.click_search()

        results = SearchResultsPage(page)
        names = results.get_all_hotel_names()

        assert len(names) > 0, "No hotel names found"
        assert all(name.strip() != "" for name in names), "Some hotel names are empty"

    @pytest.mark.parametrize("search", TEST_DATA["valid_searches"])
    def test_multiple_destinations(self, page, search):
        """Data-driven test: verify search works for multiple destinations."""
        home = HomePage(page)
        home.open()

        home.search_destination(search["destination"])
        home.select_dates(search["checkin"], search["checkout"])
        home.click_search()

        results = SearchResultsPage(page)
        results.wait_for_results()

        assert results.results_are_displayed(), (
            f"No results for destination: {search['destination']}"
        )
