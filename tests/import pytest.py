import pytest
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Get BrowserStack login credentials from environment variables
BROWSERSTACK_EMAIL = os.environ.get('BROWSERSTACK_EMAIL')
BROWSERSTACK_PASSWORD = os.environ.get('BROWSERSTACK_PASSWORD')

# Ensure that environment variables are set
assert BROWSERSTACK_EMAIL, "BrowserStack email not set in environment variables"
assert BROWSERSTACK_PASSWORD, "BrowserStack password not set in environment variables"

def test_browserstack_login_logout(selenium):
    selenium.get('https://www.browserstack.com/users/sign_in')

    # Wait for the login form
    WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.ID, 'user_email_login'))
    )

    # Enter the username and password and submit
    username_input = selenium.find_element(By.ID, 'user_email_login')
    username_input.send_keys(BROWSERSTACK_EMAIL)

    password_input = selenium.find_element(By.ID, 'user_password')
    password_input.send_keys(BROWSERSTACK_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    # Wait for 5 seconds
    time.sleep(5)
    
    try:
        hamburger_menu_toggle = WebDriverWait(selenium, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#primary-menu-toggle"))
        )
        hamburger_menu_is_present = True
    except TimeoutException:
        hamburger_menu_is_present = False

    if hamburger_menu_is_present:
        # Hamburger menu is present, click it
        hamburger_menu_toggle.click()

        # Wait for the Invite team link to become visible within the menu
        invite_users_link = WebDriverWait(selenium, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='invite-link']"))
        )
        assert invite_users_link.is_displayed(), "Invite Users link not found in menu"

        # Retrieve the link's URL
        invite_users_url = invite_users_link.get_attribute('href')
        print("Invite Users URL:", invite_users_url)

        # Sign out
        sign_out_link = WebDriverWait(selenium, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='primary-menu']/li[10]/a"))
        )
        sign_out_link.click()

    else:
        # Hamburger menu is not present, check for Invite link directly on the page
        invite_users_link = WebDriverWait(selenium, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='invite-link']"))
        )
        assert invite_users_link.is_displayed(), "Invite Users link not found on homepage"

        # Retrieve the link's URL
        invite_users_url = invite_users_link.get_attribute('href')
        print("Invite Users URL:", invite_users_url)

        # Open account menu and sign out
        account_menu_toggle = WebDriverWait(selenium, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#account-menu-toggle"))
        )
        account_menu_toggle.click()

        sign_out_link = WebDriverWait(selenium, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='sign_out_link']"))
        )
        sign_out_link.click()

    # Assert that the user is redirected to the Automate page after logout
    WebDriverWait(selenium, 10).until(
        EC.url_to_be('https://www.browserstack.com/automate')
    )
    assert selenium.current_url == 'https://www.browserstack.com/automate', "Logout unsuccessful"