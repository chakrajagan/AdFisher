import sys
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox() # Get local session of firefox 
browser.get('http://www.facebook.com') # Load page 

elem = browser.find_element_by_name("email") # Find the query box 
print elem
#elem.send_keys(sys.argv[1]) 

#ps = browser.find_element_by_name("pass") # Find the query box 
#ps.send_keys(sys.argv[2] + Keys.RETURN)
