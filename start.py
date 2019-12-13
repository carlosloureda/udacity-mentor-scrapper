# pip3 install selenium
# TODO: Make this work with new configuration
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import json
import time
# import sys
# from lib.config import get_config


def get_credentials():
    with open("./credentials.json") as json_data_file:
        return json.load(json_data_file)
    return None


def init_selenium():
    webdriver_name = "chromedriver"
    driver = webdriver.Chrome(webdriver_name)
    return driver


def authenticate(driver):
    credentials = get_credentials()
    driver.get(
        "https://auth.udacity.com/sign-in?next=https://classroom.udacity.com/authenticated")

    elem = driver.find_element(By.XPATH, "//input[@data-cy='signin-email']")
    elem.click()
    elem.send_keys(credentials["udacity"]["username"])

    elem = driver.find_element(By.XPATH, "//input[@data-cy='signin-password']")
    elem.click()
    elem.send_keys(credentials["udacity"]["password"])

    elem = driver.find_element_by_class_name(
        "button_primary__1qhjh")
    elem.click()

    # TODO: wait for something to appear on window instead of sleep
    time.sleep(10)
    # return ¿drive?


def get_info_from_dashboard(driver):
    driver.get(
        "https://mentor-dashboard.udacity.com/mentorship/overview")
    pass


def main():
    driver = init_selenium()
    authenticate(driver)
    get_info_from_dashboard(driver)


main()
