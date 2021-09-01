from selenium import webdriver

# config file :
from config import driver

# For missing values :
from math import nan

#imports for waiting :
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from math import nan

#import for actions :
from selenium.webdriver.common.action_chains import ActionChains

#own import for pretty printing html
from prettyprint import *

# ==================================== Scraping helpers ================================================
# see panel_scraper function first


def scrape_hourly_value(row):
    graph_container = row.find_element( By.CLASS_NAME, "graph-container")

    # For this we jump into graph-container div
    hourly_value = nan

    #To find hourly_value we need to hover over the last rect in our row
    #It might seem obvious to hover over the green/red boxes
    #the green/red boxes might be absent sometimes
    #hence we ignore those rects, instead we hover over the last grey vertical scale line
    #because scale lines are present no matter what

    # ===================================== Cherry-picking the target rect ============================================

    # DOM structure inside "graph-container" div :
    #  td "graph-container"
    #      3 useless nested divs
    #          svg
    #              g1
    #                g2
    #                  three g's inside which contain :
    #                      1. <g>..</g> => grey vertical scale lines                   <-- we are interested here
    #                      2. <g>..</g> => rects
    #                      3. <g>..</g> => thick base line


    # travelling level by level to our desired rects :
    svg = graph_container.find_element( By.TAG_NAME, "svg")
    g1 = svg.find_element( By.TAG_NAME, "g")
    g2 = g1.find_element( By.TAG_NAME, "g")
    g_of_rects = g2.find_element( By.TAG_NAME, "g")
    all_rects = g_of_rects.find_elements( By.TAG_NAME, "rect")

    #picking out the last rect
    target_rect = all_rects[-1]

    # ======================  We now need to move our cursor over the target_rect i.e hover ===========================

    # making an Actions object [ it helps in simulating mouse/keyboard actions ]

    hover = ActionChains(driver).move_to_element(target_rect)
    hover.perform()

    # once we hover the value-box pops up
    # now we extract the value by locating that box : [ location in DOM : g tag of class "google-visualization-tooltip" > a single text tag ]
    try:
        #sometimes our site displays no rectangle
        hourly_value = row.find_element( By.CLASS_NAME, "google-visualization-tooltip").find_element( By.TAG_NAME, "text").text
    except:
        # no rect present
        hourly_value = nan
    
    reset_hover = ActionChains(driver).move_by_offset(250,0)
    reset_hover.perform()

    return hourly_value

def scrape_metrics_row(row, include_hourly=False):
    '''Returns Pollutant deatils'''

    # Heres what the html looks like for every row :
    #   <tr class="metrics-row" style="">
    #       <td class="element-name">PM2.5</td>
    #       <td class="graph-container">.....
    #       <td class="avg-value" title="Over the last 24 hours">69</td>
    #       <td class="min-value" title="Over the last 24 hours">69</td>
    #       <td class="max-value" title="Over the last 24 hours">69</td>
    #   </tr>

    
    # extracting pollutant details from above html:
    pollutant_name = row.find_element( By.CLASS_NAME, "element-name").text
    avg_value = row.find_element( By.CLASS_NAME, "avg-value").text
    min_value = row.find_element( By.CLASS_NAME, "min-value").text
    max_value = row.find_element( By.CLASS_NAME, "max-value").text

    pollutant_values = {
        "avg_value":avg_value,
        "min_value":min_value,
        "max_value":max_value,
    }
    
    if include_hourly == True:
        pollutant_values["hourly_value"] = scrape_hourly_value(row)   
    
    return pollutant_name, pollutant_values

def scrape_pollutants(panel, include_hourly=False):

    rows = panel.find_elements( By.CLASS_NAME, "metrics-row" )
    pollutant = {}
    for row in rows:
        #try:
        name, value_dict = scrape_metrics_row(row, include_hourly)
        pollutant[name] = value_dict
        # except Exception as ex:
        #     print(str(ex))
            
    
    return pollutant

def scrape_AQI(panel):
    aqi_meter_panel = panel.find_element(By.CLASS_NAME, "aqi-meter-panel")

    #Sometimes the meter is missing with the message "Insufficient data for computing AQI"
    #In such cases an extra class "station-down" comes added to the div
    #We detect it and return a -1 as the AQI
    #[ try except , because absence of "station-down" in the if-condition below , raises index error]
    try:
        if aqi_meter_panel.get_attribute("class").split()[1] == "station-down":
            return nan
    except:
        pass

    #if meter is present :
    texts = aqi_meter_panel.find_elements( By.TAG_NAME, "text")

    ext_pprint_iter(texts, "aqi-meter-panel-texts")

    #see aqi-meter-panel-texts.html for reference
    return int(texts[1].find_element(By.TAG_NAME, "tspan").text)

def scrape_station_name_and_datetime(panel):
    tds = panel.find_elements( By.TAG_NAME, "td")
    ext_pprint_iter(tds, "aqi-meter-panel-tds")
    #see aqi-meter-panel-tds.html for reference

    station_name = tds[0].text
    #print("Station Name : "+station_name)

    datetime_string = tds[2].find_element(By.TAG_NAME, "span").text     #Tuesday, 31 Aug 2021 11:00 AM
    datetime = datetime_string.split(',')[1][1:]                        #31 Aug 2021 11:00 AM
    #print("DateTime : ", datetime)

    return station_name, datetime



# Multipurpose scraper. You can use it to scrape daily data, along with current-hour data if needed
def scrape_panel(driver, include_hourly=False):

    #Waiting for the panel to load :
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located( (By.CLASS_NAME, "aqi-panel"))
    )
    
    #find out the panel element once it's loaded
    panel = driver.find_element( By.CLASS_NAME, "aqi-panel" )

    '''
    #DEBUGGING STUFF :

    #screenshot the panel (for scraping verification purposes)
    #panel.screenshot('./img/panel.png')

    #saving entire html of panel to external file (for observation purposes)
    #ext_pprint(panel, "panel")
    '''


    #the dict that will be returned
    result = {}

    #using aur scraping helper functions
    result["StationName"], result["DateTime"] = scrape_station_name_and_datetime(panel)
    result["AQI"] = scrape_AQI(panel)
    result["Pollutants"] = scrape_pollutants(panel, include_hourly)

    return result
