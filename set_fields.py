from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By

# config file :
from config import driver

#imports for waiting :
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#import for simulating keyboard :
from selenium.webdriver.common.keys import Keys


def set_date(date_string):
    date_field = driver.find_element( By.ID, "date").find_element( By.TAG_NAME, "input")
    date_field.clear()
    date_field.send_keys(date_string+ Keys.ENTER)
    date_field.send_keys(Keys.ESCAPE)
    time_field = driver.find_element( By.ID, "time" )
    time_field.clear()
    time_field.send_keys( "23:00" + Keys.ENTER)
    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located( (By.CLASS_NAME, "aqi-panel"))
    )