# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time
import unittest
import xlrd
import json
from pyvirtualdisplay import Display
from Variables import URL, USERNAME, PASSWORD, ADJUSTRESOLUTION
from Variables import HEADERS, ACCOUNTS_API_BASE_URL, AUTH_TOKENS_API_BASE_URL
from Variables import FAVORITE_BUTTON_ELEMENT, SEARCH_BUTTON_ELEMENT, ROUTE_ONE_LOCATION_1, ROUTE_ONE_LOCATION_2, ROUTE_ASSERTION_TEXT, ADDRESS_0_TEXTBOX, ADDRESS_1_TEXTBOX
from Variables import PICK_A_ROUTE_SEARCH_BTN
from Utility import amz_headers_and_return_driver, login_to_TG_Web, get_auth_token_data, delete_all_routes_function
from Utility import navigate_to_favorites_page, navigate_to_search_page
# -*- coding: utf-8 -*-


# Function that allows Google Chrome to run on a virtual Jenkins server by providing a virtual window
def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


if ADJUSTRESOLUTION == 1:
    AdjustResolution()


def login_and_navigate_to_the_search_page(driver, waitTime):
    navigate_to_favorites_page(driver, waitTime)
    login_to_TG_Web(driver)
    navigate_to_search_page(driver, waitTime)


def create_and_assert_route_was_created(driver, waitTime):
    # Enter two locations for a saved route
    driver.find_element_by_id(ADDRESS_0_TEXTBOX).send_keys(ROUTE_ONE_LOCATION_1)
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, ADDRESS_0_TEXTBOX)))
    driver.find_element_by_id(ADDRESS_0_TEXTBOX).send_keys(Keys.RETURN)
    driver.find_element_by_id(ADDRESS_1_TEXTBOX).send_keys(ROUTE_ONE_LOCATION_2)
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, ADDRESS_1_TEXTBOX)))
    driver.find_element_by_id(ADDRESS_1_TEXTBOX).send_keys(Keys.RETURN)
    pageLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, PICK_A_ROUTE_SEARCH_BTN)))
    driver.find_element_by_id(PICK_A_ROUTE_SEARCH_BTN).click()

    # Save the link $ THIS GIVES AN ERROR!!!! SOMETIMES
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.XPATH, '//*[@id="leftPanelContent"]/div/div[3]/a')))
    driver.find_element_by_xpath('//*[@id="leftPanelContent"]/div/div[3]/a').click()  # Clicking the save this link

    # Click submit
    # Contains text "Save"?
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="save-route-form"]/button').submit()  # Clicking the submit button

    # Assert the route was saved correctly to the TG Web page
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, "favorites-content-area")))

    elementLoadWait = waitTime.until(EC.presence_of_element_located((By.CLASS_NAME, "showRoute")))
    usersFavoriteRoutes = driver.find_elements_by_class_name('showRoute')

    routeWasCreated = False

    for routeData in usersFavoriteRoutes:
        if ROUTE_ASSERTION_TEXT['location one'] and ROUTE_ASSERTION_TEXT['location two'] in routeData.text:
            routeWasCreated = True

    assert routeWasCreated

class Verify_Login_And_Saving_Routes(unittest.TestCase):


    def test_login_route_creation_and_deletion(self):

        # Take care of the amazon headers required at this stage and return a webdriver instance
        driver = amz_headers_and_return_driver()
        # Head to the agency TG Web site
        driver.get(URL)
        # Wait time variable
        waitTime = WebDriverWait(driver, 30)
        # Login and head to the page used for creating routes
        login_and_navigate_to_the_search_page(driver, waitTime)
        # create the route and assert it is saved to TG Web
        create_and_assert_route_was_created(driver, waitTime)
        # Delete all of the saved routes to clean up data from test
        delete_all_routes_function()


if __name__ == '__main__':
    unittest.main()
