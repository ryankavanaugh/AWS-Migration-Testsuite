# coding=utf-8
from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest
import xlrd
from pyvirtualdisplay import Display
from Variables import WORKBOOKNAMEDATA, USERNAME, PASSWORD, URL, ADJUSTRESOLUTION
from Utility import amz_headers_and_return_driver, login_to_TG_Web
# -*- coding: utf-8 -*-


def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


if ADJUSTRESOLUTION == 1:
    AdjustResolution()


class Verify_Login(unittest.TestCase):


    def test_login(self):

        driver = amz_headers_and_return_driver()
        driver.get(URL)
        loginElement = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'sign-in-link')))
        driver.find_element_by_id('sign-in-link').click()
        login_to_TG_Web(driver)

        # Assert that the login was successful by checking that the user's name is displayed on the main page and we are not on the login pop-up
        left_Panel_Wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))
        assert driver.find_element_by_xpath("//*[contains(text(), 'Ryan’s 511')]")


if __name__ == '__main__':
    unittest.main()
