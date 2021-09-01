from selenium import webdriver


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://app.cpcbccr.com/AQI_India/"


driver.get(url)
driver.maximize_window()