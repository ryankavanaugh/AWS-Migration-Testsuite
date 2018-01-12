# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import unittest
import json
import requests
import xlrd
from pyvirtualdisplay import Display
from Variables import NEW_PLACE_JSON_1, NEW_PLACE_JSON_2, NEW_PLACE_JSON_3, WORKBOOKNAMEDATA, FAVORITES_URL, ACCOUNTS_API_BASE_URL, AUTH_TOKENS_API_BASE_URL
from Variables import USER_EMAIL_ELEMENT, USER_PASSWORD_ELEMENT, FAVORITE_BUTTON_ELEMENT, HEADERS, ADJUSTRESOLUTION
from Variables import USERNAME, PASSWORD
from Utility import amz_headers_and_return_driver, JSON_list_creator, login_to_TG_Web, get_auth_token_data
# -*- coding: utf-8 -*-

# Function allowing Google Chrome to run on a virtual Jenkins server by providing a virtual window
def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


if ADJUSTRESOLUTION == 1:
    AdjustResolution()


def get_currently_saved_places(accountID, authToken):
    customAreasAPIUrl = ACCOUNTS_API_BASE_URL + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
    customAreaJson = requests.get(customAreasAPIUrl, headers=HEADERS)
    data = customAreaJson.json()
    if len(data) > 0:
        print 'The following places are saved for this user:'
        printCounter = 0
        while printCounter < len(data):
            print printCounter + 1
            print data[printCounter].get('name')
            printCounter += 1


def post_new_places(placesJson, authToken, accountID):
    listOfIDs = []
    for item in placesJson:
        apiUrl = ACCOUNTS_API_BASE_URL + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
        newPlacePost = requests.post(apiUrl, json=item, headers=HEADERS)
        data = json.loads(newPlacePost.content)
        id = data.get('id')
        listOfIDs.append(id)
    return listOfIDs


def login_and_head_to_favorites_page(driver):
    driver.get(FAVORITES_URL)
    login_to_TG_Web(driver)
    # Head to the favorites page
    pageLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, FAVORITE_BUTTON_ELEMENT)))
    time.sleep(2)
    signInButton = driver.find_element_by_id(FAVORITE_BUTTON_ELEMENT)
    signInButton.click()


def assert_the_correct_places_are_saved_to_TG_Web(driver):
    favoritesPageWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'user-favorite-item')))
    allFavoritesPlaces = driver.find_elements_by_class_name('user-favorite-item')
    # Create boolean variables linked to each place for testing
    BrokenBow = False
    Elmwood = False
    Callaway = False
    # Verify these places have made it to TG Web
    for favorite in allFavoritesPlaces:
        # print favorite.text
        favoritesWithAPIInfo = favorite.text
        if 'Broken Bow' in favoritesWithAPIInfo:
            BrokenBow = True
        if 'Elmwood' in favoritesWithAPIInfo:
            Elmwood = True
        if 'Callaway' in favoritesWithAPIInfo:
            Callaway = True
    # Assert that the places we created showed up in the list of favorites saved to the TG Web app
    assert BrokenBow
    assert Elmwood
    assert Callaway


def delete_places(placeIDs, authToken, accountID):
    for placeID in placeIDs:
        deleteUrl = ACCOUNTS_API_BASE_URL + str(accountID) + '/customAreas/' + str(placeID) + '?authTokenId=' + str(authToken)
        deleteItem = requests.delete(deleteUrl, headers=HEADERS)
        print deleteItem.status_code


class Verify_Saved_Places_Via_The_API(unittest.TestCase):


    def test_create_new_places(self):
        PLACES_JSON = JSON_list_creator(NEWPLACEJSON1, NEWPLACEJSON2, NEWPLACEJSON3)

        # Gather permissions data for working with the API
        USER_AUTH_DATA = get_auth_token_data()

        # Gather and print currently saved places for testing purposes
        get_currently_saved_places(USER_AUTH_DATA['accountID'], USER_AUTH_DATA['authToken'])

        # Create new places and return their unique IDs
        placeIDs = post_new_places(PLACES_JSON, USER_AUTH_DATA['authToken'], USER_AUTH_DATA['accountID'])

        # Verify new places are saved in TG Web
        driver = amz_headers_and_return_driver()
        login_and_head_to_favorites_page(driver)
        assert_the_correct_places_are_saved_to_TG_Web(driver)

        # API clean up
        delete_places(placeIDs, USER_AUTH_DATA['authToken'], USER_AUTH_DATA['accountID'])


if __name__ == '__main__':
    unittest.main()
