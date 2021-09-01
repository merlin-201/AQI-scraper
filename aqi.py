from selenium import webdriver
from selenium.webdriver.common.by import By

#config file :
from config import driver

#scrapers :
from panel_scraper import *

#setting fields :
from set_fields import *

#saving scraped data to csv :
from save_data import save

#imports for waiting :
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#dealing with missing values :
from math import nan

#imports for dealing with select tag :
from selenium.webdriver.support.select import Select

#import for actions (simulating mouse):
from selenium.webdriver.common.action_chains import ActionChains

#import for simulating keyboard :
from selenium.webdriver.common.keys import Keys

#own import for pretty printing 
from prettyprint import *



'''
# === hard coded sleep time then screenshot ===

# time.sleep(7)
# driver.maximize_window()
# driver.save_screenshot('./image.png')

'''

time.sleep(1) #just to be sure

#screenshots entire page
driver.save_screenshot('./img/entire.png')

#The site loads with a default station selected
#If we quickly change the station then panels for both stations are loaded together [ some glitch on the site developer's side ]
#so we wait for the default station's panel to load
#and once its loaded we change the station to desired one

#Waiting for the panel to load & keeps on refreshing if it doesnt load :
while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located( (By.CLASS_NAME, "aqi-panel"))
        )
        break
    except:
        driver.refresh()


# =============================================================================================================================================

set_date("12/12/2020")

#first we find the select element [ i.e  station field ]
select_station_element = driver.find_element( By.ID, "stations")

#we wrap it under a select object [ Select class provides us convenient features to play around with select tags]
select_station = Select(select_station_element)


for i in range(1, len(select_station.options) ):
    # select a station:
    select_station.select_by_index(i)

    try:
        # wait max 10 seconds for panel to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located( (By.ID, "data-available-panel"))
        )

        #dprint( scrape_panel(driver, include_hourly=True) )
        save( scrape_panel(driver) )
    except Exception as ex:
        #print("Error : ",str(ex))
        try:
            panel = driver.find_element( By.ID, "no-data-panel" )
            print("No Data Available for station : ",select_station.options[i].text)
        except:
            try:
                panel = driver.find_element( By.ID, "no-response-panel" )
                print("No Response from Server for station : ",select_station.options[i].text)
            except:
                print("Unexpected error for station : ",select_station.options[i].text)

    print('\n\n')



#dprint(scrape_panel(driver))

driver.quit()