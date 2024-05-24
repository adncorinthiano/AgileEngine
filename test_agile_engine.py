# test_agile_engine.py

import json
import logging
import os
import time
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path) as config_file:
        return json.load(config_file)

def setup_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})  # Set the viewport size to fullscreen
    page = context.new_page()
    return playwright, browser, page

def teardown_browser(playwright, browser):
    browser.close()
    playwright.stop()

def open_agileengine_website(page):
    logger.info("Opening Agile Engine website")
    page.goto("https://agileengine.com/")

def click_get_in_touch(page):
    logger.info("Clicking on 'Get in Touch' link")
    try:
        get_in_touch_link = page.locator('xpath=/html/body/div[4]/header/div[1]/div[1]/div/div/div/div[2]/div/div/div/nav/div/ul/li[5]/a')
        get_in_touch_link.click()
        page.wait_for_timeout(3000)  # Wait for 3 seconds to allow the page to load
        page.wait_for_load_state('networkidle')  # Ensure the page is fully loaded
    except Exception as e:
        logger.error("Failed to click 'Get in Touch' link: %s", e)
        raise

def fill_out_form(page, config):
    logger.info("Filling out the form")
    try:
        page.wait_for_selector('#form > div > div > div.zf-subContWrap.zf-topAlign > li > div > div.zf-nameWrapper > span > input[type=text]', timeout=30000)
        page.fill('#form > div > div > div.zf-subContWrap.zf-topAlign > li > div > div.zf-nameWrapper > span > input[type=text]', config["first_name"])
        logger.info("First name field filled")
        time.sleep(0.8)

        page.wait_for_selector('#form > div > div > div.zf-subContWrap.zf-topAlign > li > div > span > input[type=text]', timeout=30000)
        page.fill('#form > div > div > div.zf-subContWrap.zf-topAlign > li > div > span > input[type=text]', config["last_name"])
        logger.info("Last name field filled")
        time.sleep(0.8)

        page.wait_for_selector('#form > div > div > li:nth-child(4) > div.zf-tempContDiv > span > input[type=text]', timeout=30000)
        page.fill('#form > div > div > li:nth-child(4) > div.zf-tempContDiv > span > input[type=text]', config["email"])
        logger.info("Email field filled")
        time.sleep(0.8)

        page.wait_for_selector('#form > div > div > li:nth-child(5) > div.zf-tempContDiv > span > input[type=text]', timeout=30000)
        page.fill('#form > div > div > li:nth-child(5) > div.zf-tempContDiv > span > input[type=text]', config["company"])
        logger.info("Company field filled")
        time.sleep(0.8)

        page.wait_for_selector('#form > div > div > li:nth-child(6) > div.zf-tempContDiv > select', timeout=30000)
        page.select_option('#form > div > div > li:nth-child(6) > div.zf-tempContDiv > select', 'QA solutions')
        logger.info("Looking for field filled with QA solutions")
        time.sleep(0.8)

        page.wait_for_selector('#form > div > div > li:nth-child(7) > div.zf-tempContDiv > span > textarea', timeout=30000)
        page.fill('#form > div > div > li:nth-child(7) > div.zf-tempContDiv > span > textarea', config["message"])
        logger.info("Message field filled")
        time.sleep(0.8)
    except Exception as e:
        logger.error("Failed to fill out the form: %s", e)
        raise

def submit_form(page):
    logger.info("Submitting the form")
    try:
        page.wait_for_selector('#form > div > div > li.zf-fmFooter > button', timeout=30000)
        page.click('#form > div > div > li.zf-fmFooter > button')
    except Exception as e:
        logger.error("Failed to submit the form: %s", e)
        raise

def verify_form_submission(page):
    logger.info("Checking if the form was successfully submitted")
    try:
        page.wait_for_selector('#thank-you-main-section > div > h2', timeout=30000)
        success_message = page.inner_text('#thank-you-main-section > div > h2')
        assert "Thank you" in success_message
        logger.info("Form successfully submitted!")
    except Exception as e:
        # As a fallback, check the URL
        if "thank-you" in page.url:
            logger.info("Form submission verified by URL!")
        else:
            logger.error("Form submission verification failed: %s", e)
            raise
