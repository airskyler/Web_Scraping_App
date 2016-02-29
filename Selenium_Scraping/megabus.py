
# use selenium to automate web browsers across many platforms and
# use webdriver for driving a browser natively as a user would either locally or on a remote machine using the Selenium Server
# I got the top two sentence words from URL of http://www.seleniumhq.org/projects/webdriver/


from selenium.webdriver import Firefox        # import Firefox so that I can code when I am using a Firefox as a browser
from selenium.webdriver.common.by import By   # import By to find certain element in HTML code

from selenium.webdriver.support.ui import WebDriverWait    # import WebDriverWait, so that I can takes a WebDriver instance and timeout in seconds
from selenium.webdriver.support import expected_conditions # import expected_conditions to catch the code condition
from selenium.webdriver.common.keys import Keys   # import Keys for use of similar to entering keys using your keyboard


from json import dumps    # turns python data types to JSON string data
import re                 # regular expression


# bleach cleans out HTML tags
from bleach import clean


browser = Firefox()       # use FireFox as browser



def getTrips(num):

    # go to MegaBus website
    browser.get('http://us.megabus.com')

    # Looking for Minneapolis in the select drop down list
    # the value of 144 is a Minneapolis for the HTML code
    minneapolis = browser.find_element_by_css_selector('#JourneyPlanner_ddlOrigin option[value="144"]')
    minneapolis.click()     # click on it

    minneapolis.send_keys(Keys.RETURN)      # hit enter key to make sure to select Minneapolis
    wait = WebDriverWait(browser, 60)    # Time out in 60 seconds

    # Unless the next statement happens, the time out error will occur
    wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#JourneyPlanner_ddlDest option[value="100"]')))


    # Looking for Chicago in the select drop down list and click on it
    # the value of 100 is a Chicago for the HTML code
    chicago = browser.find_element_by_css_selector('#JourneyPlanner_ddlDest option[value="100"]')
    chicago.click()

    browser.implicitly_wait(3)       # wait exactly 3 seconds for information to load

    # Looking through HTML for date input field and click on it  and clear the field of text
    departureDate = browser.find_element_by_css_selector('#JourneyPlanner_txtOutboundDate')
    departureDate.click()
    departureDate.clear()


    # Type in a date and hit enter key
    departureDate.send_keys("3/0"+str(num)+"/2016")
    departureDate.send_keys(Keys.RETURN)

    browser.implicitly_wait(2)


    # Looking through HTML for something that was not a date picker
    # and then click on it, so that it will take a focus out of date picker
    browser.find_element_by_css_selector('#header').click()

    browser.implicitly_wait(3)


    # Look for search button in HTML and click on it
    browser.find_element_by_css_selector('#JourneyPlanner_btnSearch').click()

    browser.implicitly_wait(20)


    # Looking through HTML for the data about the bus trips
    items = browser.find_elements_by_css_selector('ul.journey')


    # create empty list to add data
    busTripResult=[]


    # item is a length of items for the trip for that day
    for item in items:

        # Clean out the HTML tag that were inside the text and fetching the departure information
        # and replace the text of Departs to nothing
        depatureInfo = clean(item.find_element_by_css_selector('li.two p:first-child').text, strip=True).replace('Departs', '')

        # Clean out the HTML tag that were inside the text and fetching the arrive information
        # and replace the text of Arrives with nothing
        arriveInfo = clean(item.find_element_by_css_selector('li.two p.arrive').text, strip=True).replace('Arrives', '')


        # using Regex to get the departure time and arrive time
        leave = re.match(r' [0-9]+:[0-9]+ [A-Z]+', depatureInfo).group()
        arrive = re.match(r' [0-9]+:[0-9]+ [A-Z]+', arriveInfo).group()


        # add all the bus trip data from each day to a list
        busTripResult.append({
            'from':depatureInfo.replace(leave, ''),
            'leave': leave,
            'to': arriveInfo.replace(arrive, ''),
            'arrive': arrive,
            'duration': item.find_element_by_css_selector('li.three p').text,
            'price': clean(item.find_element_by_css_selector('li.five p').text, strip=True).replace('from','')
        })



   # write the bus trip result data to the file
    with open("MegaMarch"+str(num)+"2016.json", 'w') as outfile:
        outfile.write(dumps(busTripResult))


# Call the function with each day
if __name__ == '__main__':
    for i in range(4, 5,2):
        getTrips(i)