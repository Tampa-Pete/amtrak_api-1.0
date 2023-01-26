import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.common.action_chains import ActionChains
import string
import itertools

def getstationcodes():
    letters = list(string.ascii_uppercase)
    tripleletter = list(itertools.product(letters,repeat=3))
    codes = [''.join(triplet) for triplet in tripleletter]

    return codes

def gscstr(driver, element, xcode, input, noresult):    #element = webdriver.Chrome._web_element_cls
    # gets resulting xcode table from element
    element.send_keys(input)
    
    result_ul = element.find_element(By.XPATH, xcode)
    WebDriverWait(driver, timeout=5).until(expected_conditions.visibility_of(result_ul))
    
    result_li = result_ul.find_elements(By.TAG_NAME, 'li')

    if result_li[0].text == noresult:
        return None
    return [(r.text) for r in result_li]

def gsclist(driver, element, xcode, input, noresult):
    # gets list of data by appending from string method
    results = {}
    for i in input:
        r = gscstr(driver, element, xcode, i, noresult)
        if r is not None:
            results[i] = r
        element.click()
        element.clear()

    return results

def gscresult(driver, element, xcode, input):
    # determines {input} datatype

    noresult = 'There are no routes or stations that match your search.'

    if isinstance(input,str):   #returns a list of possible results
        result = gscstr(driver, element, xcode, input, noresult)
    elif isinstance(input,list):    #returns a dictionary of listed results
        result = gsclist(driver, element, xcode, input, noresult)
        #print(input)
    else:
        raise TypeError
    return result

def getstationcodewrapper(stationcode = 'ABE'):
    site = 'https://www.amtrak.com/services/maps.trainlocation.html'
    field_xcode = '//*[@id="search_field"]'
    button_xcode = '//*[@id="search_button"]'
    results_xcode = '//*[@id="ui-id-1"]'

    driver = webdriver.Chrome('/Users/plau/Documents/Code/python/Selenium_Drivers/chromedriver')
    driver.get(site)
    driver.implicitly_wait(10)

    field = driver.find_element(By.XPATH, field_xcode)
    button = driver.find_element(By.XPATH, button_xcode)

    '''field.send_keys(stationcode)
    result_ul = driver.find_element(By.XPATH, results_xcode)
    result_li = result_ul.find_elements(By.TAG_NAME, 'li')
    results = [(i.text) for i in result_li]'''
    results = gscresult(driver, field, results_xcode, stationcode)

    # Close the SafariDriver instance
    driver.close()

    #Remove null result

    return results

def getstations():
    codes = getstationcodes()
    #results = {}

    #for x in range(3):  # get values from station code list
    results = getstationcodewrapper(codes[1:100])

    print(results,sep='\n')
    #write to file
    '''with open('output.txt','w') as f:
        index = 0
        while index < len(codes):
            f.write(codes[index]+'\n')
            index+=1'''


getstations()

'''
import requests
from bs4 import BeautifulSoup

status_id = {
    '_ngcontent-rqc-c304':'',
    'data-julie':'train_status',
    'hidden':''
}
search = 'STATUS'

# Find the amtrak website
response = requests.get(site)

#parse HTML content
soup = BeautifulSoup(response.content, 'html.parser')

#raw HTML
html = response.text

#writing raw html to text
with open('output.txt', 'w') as f:
    f.write(html)
    f.close()

buttons = soup.findAll('button')

for b in buttons:
    if search in b.text:
        print(b.attrs)
'''