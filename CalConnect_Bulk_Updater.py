# Selenium is the package that allows us to automate our web browser
from selenium import webdriver

# Webdriver_manager assures we have the correct chromedriver for selenium to work, if we dont, it downloads it.
from webdriver_manager.chrome import ChromeDriverManager

# Options allows us to change the webdriver options like managing downloads or hiding the browser window
from selenium.webdriver.chrome.options import Options

# For error handling
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import Credentials


class BulkUpdater:
    def __init__(self):

        # CalConnect Sign On Info
        self.username = Credentials.login['username']
        self.password = Credentials.login['password']
        self.list_url = Credentials.login['list_url']

        # Initialize Options
        self.options = Options()
        self.options.headless = False  # headless = True hides the chrome browser running in the background, set this to
                                       # false if you want to watch the script step through the website
        self.options.add_argument("--disable-notifications")    # disables annoying allow notifications pop up that messes stuff up
        self.options.add_argument("disable-popup-blocking")
        self.options.add_argument("test-type")

        # Initialize webdriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        # if page takes longer than 1500 seconds to load it times out...
        self.driver.set_page_load_timeout(1500)

    def load(self):
        """
        Load CalConnect web site
        :return: Null
        """
        # CalConnect Login Screen
        self.driver.get("https://auth.calconnect.cdph.ca.gov/auth/XUI/#login/")

    def login(self):
        """
        This functions locates the username/password fields, enters specified username/password combo and clicks login
        :return: Null
        """
        # This block waits until the username/password and login fields are loaded before proceeding
        while True:
            try:
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='idToken1']")))
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='idToken2']")))
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='loginButton_0']")))
                break
            except TimeoutException:
                print("Timeout Exception: Page elements took too long to load")

        # Find username field
        login_field = self.driver.find_element_by_xpath("//*[@id='idToken1']")

        # Enter username
        login_field.send_keys(self.username)
        print("DEBUG: entered username")

        # Find password field
        password_field = self.driver.find_element_by_xpath("//*[@id='idToken2']")

        # Enter password
        password_field.send_keys(self.password)
        print("DEBUG: entered password")

        # Find login button
        login_button = self.driver.find_element_by_xpath("//*[@id='loginButton_0']")

        # Login
        login_button.click()
        print("DEBUG: clicked login")

    def consent(self):
        """
        This function clicks CC Consent button upon login
        :return:
        """
        # Wait for page to load
        while True:
            try:
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='idToken2_0']")))
                break
            except TimeoutException:
                print("Timeout Exception: Page elements took too long to load")

        # Locate and Click Consent Button
        consent_button = self.driver.find_element_by_xpath("//*[@id='idToken2_0']")
        consent_button.click()

    def production(self):
        """
        This function selects the CalConnect Production Environment after logging in
        :return:
        """
        # Wait for page to load
        while True:
            try:
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='myApplication_0']/a")))
                break
            except TimeoutException:
                print("Timeout Exception: Page elements took too long to load")
        # Locate and click production link
        production_link = self.driver.find_element_by_xpath("//*[@id='myApplication_0']/a")
        production_link.click()

    def load_list(self):
        """
        This function loads the list created for Incidents that need bulk update
        It will then iterate through that list, change Process Status + to "Closed by LHJ", and save
        :return:
        """
        # Action is required to simulate mouse hover
        action = ActionChains(self.driver)

        # This is our current window, click back to it

        currentWindow = self.driver.current_window_handle
        self.driver.switch_to.window(currentWindow)

        # Load List
        # This is a list that must be created of all the incident ids you want to update. Currently,
        # the target column to be updated is the 3rd column.
        self.driver.get(self.list_url)
        time.sleep(30)
        # Wait for page to load
        while True:
            try:
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='brandBand_1']/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table")))
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='brandBand_1']/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table/tbody")))
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.TAG_NAME, "tr")))
                WebDriverWait(self.driver, 50).until(
                    EC.presence_of_element_located((By.TAG_NAME, "td")))
                break
            except TimeoutException:
                print("Timeout Exception: Page elements took too long to load")

        # Identify data table presented in list
        table = self.driver.find_element_by_xpath("//*[@id='brandBand_1']/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table")
        # Get table rows
        table_rows = table.find_elements(By.TAG_NAME, "tr")
        inline_edit = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[1]/div[2]/div[3]/force-list-view-manager-button-bar/div/div[2]/lightning-button-icon/button")
        # Iterate through table rows, starting at 1, 0 is an empty row?
        for i in range(1, len(table_rows)):
            time.sleep(.5)
            self.driver.switch_to.window(currentWindow)
            print("Iterating row: ", i)

            # 3rd cell element (column)
            xpath = "/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table/tbody/tr[" + str(i) + "]/td[4]"


            # Edit button in 3rd cell
            button = xpath + "/span/span[2]/button"
            # Menu produced from button click
            dropdown_menu = xpath + "/div"

            # Locate target elements
            self.driver.switch_to.window(currentWindow)
            pStatus = self.driver.find_element_by_xpath(xpath)

            # Simulate hovering mouse over pStatus cell, and click on edit button
            #hover = ActionChains(self.driver).move_to_element(pStatus).pause(1).move_to_element(self.driver.find_element_by_xpath(button)).click()
            #hover.perform()

            self.driver.switch_to.window(currentWindow)
            pStatus.click()
            self.driver.switch_to.window(currentWindow)
            pStatus.click()
            print("Cell Click")
            self.driver.switch_to.window(currentWindow)
            inline_edit.click()
            print("Edit click, waiting for menu to load")
            while True:
                try:
                    WebDriverWait(self.driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, dropdown_menu)))
                    break
                except TimeoutException:
                    print("Timeout Exception: Page elements took too long to load")


            print("Menu loaded, opening")
            # Simulate menu open
            self.driver.switch_to.window(currentWindow)
            menu = self.driver.find_element_by_xpath(dropdown_menu)
            menu.click()

            print("Waiting for menu elements to load")
            # Wait for menu elements to load
            while True:
                try:
                    WebDriverWait(self.driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[8]")))
                    break
                except TimeoutException:
                    print("Timeout Exception: Page elements took too long to load")

            # Locate and select "Closed by LHJ option"
            # IF YOU WANT TO EDIT A DIFFERENT FIELD THIS XPATH WILL MOST LIKELY NEED TO BE UPDATED #
            print("Changing selected variable")
            self.driver.switch_to.window(currentWindow)
            closed_by_lhj = self.driver.find_element_by_xpath("/html/body/div[8]/div/ul/li[8]")
            closed_by_lhj.click()

        # DONT UNCOMMENT THIS UNTIL YOU HAVE RAN IT ONCE AND KNOW IT IS CHANGING THE FIELD YOU WANT TO WHAT YOU WANT IT TO
        # Locate and click save
        print("Saving")
        #save_button = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/button[2]")
        #save_button.click()


    def close(self):
        """
        This function closes the web browser
        :return: Null
        """
        self.driver.quit()


if __name__ == "__main__":
    d = BulkUpdater()    # initialize our updater
    d.load()    # load calconnect
    d.login()   # login to calconnect
    d.consent()     # consent to terms
    d.production()  # load production environment
    d.load_list()   # load list of incident id's to change and change them!
    time.sleep(50)   # sleep to allow time to save
    d.close()       # close chrome
