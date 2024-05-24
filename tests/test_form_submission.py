# tests/test_form_submission.py

import pytest
from test_agile_engine import (load_config, setup_browser, teardown_browser,
                               open_agileengine_website, click_get_in_touch,
                               fill_out_form, submit_form, verify_form_submission)

@pytest.fixture(scope="module")
def browser():
    playwright, browser, page = setup_browser()
    yield page
    teardown_browser(playwright, browser)

def test_open_agileengine_website(browser):
    open_agileengine_website(browser)
    assert "AgileEngine" in browser.title()

def test_form_submission(browser):
    config = load_config()
    open_agileengine_website(browser)
    click_get_in_touch(browser)
    fill_out_form(browser, config)
    submit_form(browser)
    verify_form_submission(browser)
