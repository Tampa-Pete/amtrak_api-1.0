import csv
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
import string
import itertools
import logging

class amtrak_train_station:
    def __init__(self):
        self.number = 4
        self.route = 'Southwest Chief'
        self.scheduled = 'February 6, 2023 11:20AM MT'

class amtrak_station:
    def __init__(self):
        self.name = 'ALBUQUERQUE, NM'
        self.code = 'ABQ'
        self.address = '320 1st Street SW'
        self.amenities = 'Station Building (with waiting room)'
        self.routes = [amtrak_train_station.__init__]   #change to trains needing stations rather than this


#getting logger for this code, not Selenium, see: https://docs.python.org/3/library/logging.html#logrecord-attributes
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('extract_amtrak.log')
formatter = logging.Formatter('%(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#train/station information

def reset_map(driver):
    logger.info("resetting map")
    driver.find_element(By.ID, 'map_reset_button').click()
    return

def train_number(t):
    m = re.search('^/d{1,4}',t)
    assert m
    logger.info(f"train_number found {m} in {t}")
    return m.group(0)

def extract_info_station(element = webdriver.Chrome._web_element_cls):
    station_name = element.find_element(By.ID, 'iwsIW_left_content').text
    station_code = element.find_element(By.ID, 'iwsIW_right_content').text
    station_address = element.find_element(By.ID, 'iwsIW_mid_content').text
    station_next_train = element.find_element(By.ID, 'stationStatus_arr').get_attribute('innerHTML')
    logger.info(f"got station {station_name}")
    return {
        'sname': station_name,
        'scode': station_code,
        'saddress': station_address,
        'snexttrain': station_next_train
    }

def extract_info_train(element = webdriver.Chrome._web_element_cls):
    #multiple trains can be part of the same route at one time
    try:
        element.find_element(By.ID, 'iwsIW_mid_content_search_results').click
        train_results = element.find_elements(By.ID, 'search_train_').text
        for train in train_results:
            logger.info(f"found train element: {train.text}")
    except NoSuchElementException:
        train = element.find_element(By.ID, 'iwsIW_left_content').text
        train_num = train_number(train)
        train_name = train.lstrip(f"{train_num} ")  #removes train number and whitespace
        arrival = element.find_element(By.ID, 'iwsIW_mid_content')
        train_dest = arrival.find_element(By.CLASS_NAME, 'if_train_info_mid_o').text
        train_arrival = arrival.find_element(By.CLASS_NAME, 'text_blue float_left bold').text
        train_delay = arrival.find_element(By.CLASS_NAME, 'text_black float_right if_train_info_comment').text
    logger.info(f"got train {train_num} named: {train_name}")
    return {
        'tnum': train_num,
        'tname': train_name,
        'destination': train_dest,
        'arrival': train_arrival,
        'delay': train_delay
    }

def extract_info_window(driver = webdriver.Chrome):
    info_window_xcode = '//*[@id="map_canvas"]/div/div/div[2]/div[2]/div/div[4]/div[2]'
    header_id = 'iwsIW_left_content'

    try:
        info_window_element = driver.find_element(By.XPATH, info_window_xcode)
        WebDriverWait(driver, timeout=5).until(expected_conditions.visibility_of(info_window_element))
    except NoSuchElementException:
        logger.error("info_window not found")
        raise AssertionError
    assert info_window_element.get_attribute('class') == 'infowindow_wrapper'
    #result_ul = element.find_element(By.XPATH, xcode)
    #WebDriverWait(driver, timeout=5).until(expected_conditions.visibility_of(result_ul))

    info_header = info_window_element.find_element(By.ID, header_id)
    try:
        train_info = extract_info_train(info_window_element)
        logger.info(f"found train info: {train_info}")
        return train_info
    except AssertionError:
        #info_header is a station
        station_info = extract_info_station(info_window_element)
        logger.info(f"found station info {station_info}")
        return station_info

def check_result(i, c):
    pass
    '''if c.find('('+i+')') > 0:
        return [c]
    else:
        return None'''


def getstationcodes():
    letters = list(string.ascii_uppercase)
    tripleletter = list(itertools.product(letters,repeat=3))
    codes = [''.join(triplet) for triplet in tripleletter]

    return codes

def gscstr(driver, element, xcode, input, noresult):    #element = webdriver.Chrome._web_element_cls
    # gets resulting xcode table from element
    element.send_keys(input)

    result_ul = element.find_element(By.XPATH, xcode)
    try:
        WebDriverWait(driver, timeout=5).until(expected_conditions.visibility_of(result_ul))
    except TimeoutException:
        logger.error("timeout error, handled by resetting map")
        reset_map(driver)
        return gscstr(driver, element, xcode, input, noresult)
    result_li = result_ul.find_elements(By.TAG_NAME, 'li')

    if result_li[0].text == noresult:
        return None
    #for r in result_li:    #will use this to check results later
    #    result = check_result(input, r.text)
    #result_li[0].click()
    return [r.text for r in result_li] #result

def print_csv(i, d):
    pass
    '''with open('output.csv','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([i,d.list])'''

def gsclist(driver, element, xcode, input, noresult):
    # gets list of data by appending from string method
    results = {}
    for i in input:
        element.click()
        element.clear()
        r = gscstr(driver, element, xcode, i, noresult)
        if r is not None:
            results[i] = r
            try:
                logger.info(f"looking for: {i}")
                #print_csv(input, extract_info_window(driver))  #not doing this yet
            except AssertionError:
                continue

    return results

def check_code(code = str):
    #makes sure code is either a number or three letters
    no_train = 'There are no routes or stations that match your search.'
    no_station = 'There are no active trains that match your search.'
    
    if isinstance(code,list):
        return check_code(code[0])
    elif isinstance(code,int):
        return no_train
    elif code.isdigit():
        return no_train
    elif code.isalpha():
        return no_station if code is re.match('\s{3}',code) else None #check this!!!
    else:
        return None

def gscresult(driver, element, xcode, input):
    noresult = check_code(input)
    assert(noresult)    #should throw exception if None
  
    if isinstance(input,str):   #returns a list of possible results
        result = gscstr(driver, element, xcode, input, noresult)
    elif isinstance(input,list):    #returns a dictionary of listed results
        result = gsclist(driver, element, xcode, input, noresult)
    else:
        raise TypeError
    return result

def getstationcodewrapper(code = 'ABE'):
    site = 'https://www.amtrak.com/services/maps.trainlocation.html'
    field_xcode = '//*[@id="search_field"]'
    button_xcode = '//*[@id="search_button"]'
    results_xcode = '//*[@id="ui-id-1"]'

    driver = webdriver.Chrome('/Users/plau/Documents/Code/python/Selenium_Drivers/chromedriver')
    #download new drivers here: https://sites.google.com/chromium.org/driver/downloads?authuser=0
    driver.get(site)
    driver.implicitly_wait(10)

    field = driver.find_element(By.XPATH, field_xcode)
    button = driver.find_element(By.XPATH, button_xcode)

    '''field.send_keys(stationcode)
    result_ul = driver.find_element(By.XPATH, results_xcode)
    result_li = result_ul.find_elements(By.TAG_NAME, 'li')
    results = [(i.text) for i in result_li]'''
    results = gscresult(driver, field, results_xcode, code)

    # Close the SafariDriver instance
    driver.close()

    #Remove null result

    return results

def getstations():
    codes = getstationcodes()
    example = codes #[25:35] #ABE
    results = getstationcodewrapper(example)
    if isinstance(results,list):
        results = {example:results} #returns a dictionary
    return results

def print_stations(list, file = 'output.txt'):  #previously no passed variables
    pass
    #need to adjust below to match any list input
    '''stations = getstations()
    #write to file
    with open('output.txt','w') as f:
        writer = csv.writer(f)
        for key in stations.keys():
            row = [key] + stations[key]
            writer.writerow(row)'''

print("started at: %s" % datetime.now())
#print_stations()
codes = [*range(10)]
trains = getstationcodewrapper(codes)
with open('output.txt','w') as fout:
    writer = csv.writer(fout)
    for key in trains.keys():
        row = [key] + trains[key]
        writer.writerow(row)
print("ended at: %s" % datetime.now())
