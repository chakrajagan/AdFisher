import sys
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox() # Get local session of firefox 
browser.get('http://www.facebook.com') # Load page 

elem = browser.find_element_by_name("email") # Find the query box 
elem.send_keys(sys.argv[1]) 

ps = browser.find_element_by_name("pass") # Find the query box 
ps.send_keys(sys.argv[2] + Keys.RETURN)

driver = browser
file = "test.txt"

#driver.get('http://bbc.com/news')
driver.set_page_load_timeout(60)
"""
driver.get('automall.com')
driver.set_page_load_timeout(60)
driver.get('prostreetonline.com')
driver.set_page_load_timeout(60)
driver.get('passwordjdm.com')
driver.set_page_load_timeout(60)
driver.get('australianmusclecarsales.com.au')
driver.set_page_load_timeout(60)
driver.get('autosearcher.com')
"""

driver.get('http://www.facebook.com')

#els = driver.find_elements_by_css_selector("div#bbccom_adsense_mpu div ul li")
els = driver.find_elements_by_class_name("ego_unit")
#print(len(els))
for el in els:
	t = el.find_elements_by_class_name("_5vwh")
	title = t[0].find_element_by_css_selector("strong").get_attribute('innerHTML')
	
	l = el.find_elements_by_class_name("_4xvg")
	link = ""
	if len(l) > 0:
		link = l[0].get_attribute('innerHTML')

	b = el.find_elements_by_class_name("_5vwk")
	content = b[0].get_attribute('innerHTML')

	oneAd = "ad||"+title+"||"+link+"||"+content
	print(oneAd)
	#ps = el.find_elements_by_css_selector("p")
	#b = ps[0].get_attribute('innerHTML')
	#l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
	#t = "ad||"+t+"||"+l+"||"+b
	#fo = open(file, "a")
	#fo.write(t + '\n')
	#fo.close()
sys.stdout.write(".")
sys.stdout.flush()
