"""
Pytest configuration for Playwright tests

This file sets up Playwright fixtures for browser testing.
"""

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser():
    """Create a browser instance"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Create a new page for each test"""
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()
