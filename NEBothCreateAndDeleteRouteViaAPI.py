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
from Variables import WORKBOOKNAMEDATA, CREATE_ROUTE_JSON, ADJUSTRESOLUTION, WORKBOOK, WORKSHEET, URL, USERNAME, PASSWORD, HEADERS, FAVORITE_BUTTON_ELEMENT
from Variables import ACCOUNTS_API_BASE_URL, AUTH_TOKENS_API_BASE_URL
from Utility import login_to_TG_Web, amz_headers_and_return_driver, get_auth_token_data, delete_all_routes_function
from Utility import navigate_to_favorites_page
# -*- coding: utf-8 -*-


# Function allowing Google Chrome to run on a virtual Jenkins server by providing a virtual window
def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


if ADJUSTRESOLUTION == 1:
    AdjustResolution()


def post_place_to_api(placeJson, authToken, accountID):
    apiPostUrl = ACCOUNTS_API_BASE_URL + str(accountID) + '/trips?authTokenId=' + str(authToken)
    newPlacePost = requests.post(apiPostUrl, json=placeJson, headers=HEADERS)


class Verify_Login_And_Saving_Routes_Via_API(unittest.TestCase):


    def test_login_route_creation_and_deletion(self):
        userAuthData = get_auth_token_data()
        post_place_to_api(CREATE_ROUTE_JSON, userAuthData['authToken'], userAuthData['accountID'])
        driver = amz_headers_and_return_driver()

        waitTime = WebDriverWait(driver, 30)

        # Navigate to TG Web
        driver.get(URL)

        navigate_to_favorites_page(driver, waitTime)

        login_to_TG_Web(driver)

        # Navigate to favorite's page
        time.sleep(1)
        driver.find_element_by_id(FAVORITE_BUTTON_ELEMENT).click()

        # Gather saved routes data
        elementLoadWait = waitTime.until(EC.presence_of_element_located((By.CLASS_NAME, "showRoute")))
        usersFavoriteRoutes = driver.find_elements_by_class_name('showRoute')

        # Assert route was created in TG Web
        routeWasCreated = False

        for route in usersFavoriteRoutes:
            if 'Henderson to Minden' in route.text:
                routeWasCreated = True

        # Clean up data from test before test assertion
        delete_all_routes_function()

        # Assert statement
        assert routeWasCreated


if __name__ == '__main__':
    unittest.main()