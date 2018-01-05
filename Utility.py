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
from Variables import USERNAME, PASSWORD, URL, ADJUSTRESOLUTION
from Variables import USER_EMAIL_ELEMENT, USER_PASSWORD_ELEMENT, HEADERS, FAVORITE_BUTTON_ELEMENT, SEARCH_BUTTON_ELEMENT
from Variables import AUTH_TOKENS_API_BASE_URL, ACCOUNTS_API_BASE_URL


def amz_headers_and_return_driver():
    options = webdriver.ChromeOptions()
    options.add_extension('ModHeader_v2.1.2.crx')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("chrome-extension://idgpnmonknjnojddfkpgkljpfnnfcklj/icon.png")
    driver.execute_script(
        "localStorage.setItem('profiles', JSON.stringify([{                " +
        "  title: 'Selenium', hideComment: true, appendMode: '',           " +
        "  headers: [                                                      " +
        "    {enabled: true, name: 'Host', value: 'hb.511.nebraska.gov', comment: ''}, " +
        "  ],                                                              " +
        "  respHeaders: [],                                                " +
        "  filters: [{enabled: true, type: 'urls', urlPattern : '*//*crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/*' , comment: ''},]                                                     " +
        "}]));")
    return driver


def JSON_list_creator(JSON1, JSON2, JSON3):
    PLACES_JSON = []
    PLACES_JSON.append(JSON1)
    PLACES_JSON.append(JSON2)
    PLACES_JSON.append(JSON3)
    return PLACES_JSON


def login_to_TG_Web(driver):
    loginElement2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, USER_EMAIL_ELEMENT)))
    driver.find_element_by_id(USER_EMAIL_ELEMENT).send_keys(USERNAME)
    driver.find_element_by_id(USER_PASSWORD_ELEMENT).send_keys(PASSWORD)
    driver.find_element_by_id(USER_PASSWORD_ELEMENT).submit()


def get_auth_token_data():
    USER_AUTH_DATA = {}
    userInfo = {"userId": USERNAME, "password": PASSWORD}
    authTokenURL = AUTH_TOKENS_API_BASE_URL

    myResponse = requests.post(authTokenURL, json=userInfo, headers=HEADERS)
    jData = json.loads(myResponse.content)
    authToken = jData.get('id')
    accountID = jData.get('accountId')

    USER_AUTH_DATA['authToken'] = authToken
    USER_AUTH_DATA['accountID'] = accountID

    return USER_AUTH_DATA


def delete_all_routes_function():
    userAuthData = get_auth_token_data()
    #   Get all saved routes and delete them
    customAreasAPIUrl = ACCOUNTS_API_BASE_URL + str(userAuthData['accountID']) + '/trips?authTokenId=' + str(userAuthData['authToken'])
    customAreaJson = requests.get(customAreasAPIUrl, headers=HEADERS)
    data = customAreaJson.json()
    indexNumber = 0
    if len(data) > 0:
        for x in data:
            routeID = data[indexNumber].get('id')
            deleteUrl = ACCOUNTS_API_BASE_URL + str(userAuthData['accountID']) + '/trips/' + str(routeID) + '?authTokenId=' + str(userAuthData['authToken'])
            deleteItem = requests.delete(deleteUrl, headers=HEADERS)
            indexNumber += 1


def navigate_to_favorites_page(driver, waitTime):
    pageLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, FAVORITE_BUTTON_ELEMENT)))
    favoritesButton = driver.find_element_by_id(FAVORITE_BUTTON_ELEMENT)
    favoritesButton.click()


def navigate_to_search_page(driver, waitTime):
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, SEARCH_BUTTON_ELEMENT)))
    searchButton = driver.find_element_by_id(SEARCH_BUTTON_ELEMENT)
    clickLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, SEARCH_BUTTON_ELEMENT)))
    time.sleep(2)
    searchButton.click()