import pytest
from playwright.sync_api import sync_playwright, Page


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="en-US",
    )
    page = context.new_page()

    # Automatically dismiss sign-in popup on every page navigation
    page.on("load", lambda: _dismiss_sign_in_popup(page))

    yield page
    context.close()


def _dismiss_sign_in_popup(page: Page):
    """
    Attempts to close the Booking.com sign-in popup/modal.
    Tries multiple known selectors silently — safe to call even if popup is absent.
    """
    selectors = [
        '[aria-label="Dismiss sign-in info."]',                         # Most common modal X
        'button[data-testid="header-sign-in-prompt-dismiss-button"]',   # Alternate modal X
        'button[data-testid="sign-in-dismiss"]',                        # Another known variant
        'button[aria-label="Close"]',                                   # Generic modal close
        '[data-testid="sign-in-banner-close-button"]',                  # Banner variant
        '.bui-modal__close',                                            # Booking UI modal class
        '.modal-mask-close',                                            # Legacy selector
    ]

    for selector in selectors:
        try:
            element = page.locator(selector).first
            if element.is_visible(timeout=2000):
                element.click()
                return  # Stop after first successful dismissal
        except Exception:
            continue  # Selector not found — try the next one
