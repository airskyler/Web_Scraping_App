
# use selenium to automate web browsers across many platforms and
# use webdriver for driving a browser natively as a user would either locally or on a remote machine using the Selenium Server
# I got the top two sentence words from URL of http://www.seleniumhq.org/projects/webdriver/


from selenium.webdriver import Firefox         # import Firefox so that I can code when I am using a Firefox as a browser
from selenium.webdriver.common.by import By    # import By to find certain element in HTML code
from selenium.webdriver.support.ui import WebDriverWait     # import WebDriverWait, so that I can takes a WebDriver instance and timeout in seconds
from selenium.webdriver.support import expected_conditions  # import expected_conditions to catch the code condition
from selenium.webdriver.common.keys import Keys   # import Keys so that code can press enter key, similar to pressing key on keyboard


# importing dumps to turns python data types to JSON string data
from json import dumps


# use Firefox as a browser
browser = Firefox()


def getTrips():

    # open GreyHound website
    browser.get('http://www.greyhound.com')
    browser.maximize_window()


    # find the HTML id name with "locationFrom"
    locationFrom = browser.find_element_by_id('fromLocation')
    locationFrom.send_keys("Minneapolis")   # type Minneapolis text into form
    locationFrom.send_keys(Keys.RETURN)     # press enter

    wait = WebDriverWait(browser, 40)    #  wait till list element on click available
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#fromBusStops > li[onclick]')))

    # looking through HTML for first list element
    minneapolis = browser.find_element_by_css_selector('#fromBusStops li[onclick]:first-child')
    minneapolis.click()    # then click on it


    # find the HTML id name with "locationTo"
    locationTo = browser.find_element_by_id('toLocation')
    locationTo.send_keys("Chicago")         # type Chicago text into form
    locationTo.send_keys(Keys.RETURN)       # press enter


    wait = WebDriverWait(browser, 30)    #  wait till list element on click available
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#toBusStops > li[onclick]')))

    # looking through HTML for first list element
    chicago = browser.find_element_by_css_selector('#toBusStops li[onclick]:first-child')
    chicago.click()        # then click on it


    # Looking in HTML for date picker
    datePick = browser.find_element_by_css_selector('input#datepicker-from.form-control.dp')
    datePick.click()     # then click on it


    # Looking through HTML for date picker table data with the class of new and day
    items = browser.find_elements_by_css_selector('td.new.day')
    for item in items:
        if item.text==str(1):   # looking for the date March 1st
            item.click()        # and click on it
            break

    browser.find_element_by_id('fare-search-btn').click()   # click the search button

    # wait exactly 40 seconds
    browser.implicitly_wait(40)

    for number in range(1, 8): # Try to get bus trip data for date between March 1st through March 7th

        # fetching the information for bus trip on GreyHound web page for each day
        sections = browser.find_elements_by_css_selector('section.fare-row')


        greyhoundResult = []  # create empty list to append data to
        for section in sections:

            # fetching the data for every bus trip for each day and add that data to the list
            greyhoundResult.append({'from':section.find_element_by_css_selector('li.trip-from p.trip-location').text,
                'leave': section.find_element_by_css_selector('li.trip-from p.trip-time').text,
                'price': section.find_element_by_css_selector('td.trip-price span.price').text,
                'schedule': section.find_element_by_css_selector('li.trip-detail p.trip-schedule span').text,
                'duration': section.find_element_by_css_selector('li.trip-detail p.trip-duration').text,
                'transfers': section.find_element_by_css_selector('li.trip-detail p.trip-transfers').text,
                'to':section.find_element_by_css_selector('li.trip-to p.trip-location').text,
                'arrive': section.find_element_by_css_selector('li.trip-to p.trip-time').text })


       # make a file to output the data to
        with open('March'+ str(number) +'2016.json', 'w') as outfile:
            outfile.write(dumps(greyhoundResult))   # write the output to the file


        # Looking through HTML for the next date
        element = browser.find_element_by_css_selector('li#selected-date + li a')
        element.click()      # then click on it
        browser.implicitly_wait(10)
        browser.refresh()    # refreshing the browser


# call the getTrips function
if __name__== '__main__':
    getTrips()
