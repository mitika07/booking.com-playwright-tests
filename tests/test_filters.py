import json
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


with open("test_data/search_data.json") as f:
    TEST_DATA = json.load(f)


class TestFilters:
    """
    Tests covering filtering on the search results page.
    """

    @pytest.fixture(autouse=True)
    def perform_search(self, page):
        """Shared setup: perform a search before each filter test."""
        search = TEST_DATA["valid_searches"][0]
        home = HomePage(page)
        home.open()
        home.search_destination(search["destination"])
        home.select_dates(search["checkin"], search["checkout"])
        home.click_search()

        self.results = SearchResultsPage(page)
        self.results.wait_for_results()

    def test_results_exist_before_filtering(self, page):
        """Baseline: confirm results exist before applying any filter."""
        assert self.results.results_are_displayed()

    def test_filter_by_5_stars_reduces_results(self, page):
        """Applying 5-star filter should reduce or keep the same result count."""
        initial_count = self.results.get_result_count()
        self.results.filter_by_stars(5)
        self.results.wait_for_results()
        filtered_count = self.results.get_result_count()

        assert filtered_count <= initial_count, (
            "Filtered results should be <= unfiltered results"
        )

    def test_filter_by_3_stars(self, page):
        """3-star filter should still return results for a major city."""
        self.results.filter_by_stars(3)
        self.results.wait_for_results()
        assert self.results.results_are_displayed(), "Expected results after 3-star filter"

    def test_sort_by_price(self, page):
        """Sorting by price should not break results display."""
        self.results.sort_by("price (lowest first)")
        self.results.wait_for_results()
        assert self.results.results_are_displayed(), "Results disappeared after sorting"
