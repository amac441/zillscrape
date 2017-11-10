from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from utils.timeout import timeout
# Timeout a long running function with the default expiry of 10 seconds.
import sys


class SeleniumUtil:
    DELAY_BETWEEN_ELEMENT_SEARCH = 1
    WAIT_ELEMENT_CLASS_TYPE = "wait_for_element_with_class"
    WAIT_ELEMENT_ID_TYPE = "wait_for_element_with_id"
    WAIT_ELEMENT_NAME_TYPE = "wait_for_element_with_name"
    WAIT_ELEMENT_TAG_NAME_TYPE = "wait_for_element_with_tag_name"
    MAX_WAITING_ATTEMPTS = 60

    @staticmethod
    def get_element_after_loading(driver, search_element, search_type=WAIT_ELEMENT_ID_TYPE):
        attempts_amount = 0
        element = None
        # try:
        #     wd=driver.page_source
        #     wdlist=wd.split("<")
        # except:
        #     pass
        while attempts_amount < SeleniumUtil.MAX_WAITING_ATTEMPTS:
            try:
                if search_type == SeleniumUtil.WAIT_ELEMENT_NAME_TYPE:
                    element = driver.find_element_by_name(search_element)
                elif search_type == SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE:
                    element = driver.find_element_by_class_name(search_element)
                elif search_type == SeleniumUtil.WAIT_ELEMENT_ID_TYPE:
                    element = driver.find_element_by_id(search_element)
                elif search_type == SeleniumUtil.WAIT_ELEMENT_TAG_NAME_TYPE:
                    element = driver.find_element_by_tag_name(search_element)
                return element
            except NoSuchElementException:
                attempts_amount += 1
                print('\nWait_for_elements_loading -> We are still waiting for element', search_element, "Attempts =",
                      attempts_amount)
                sleep(SeleniumUtil.DELAY_BETWEEN_ELEMENT_SEARCH)
        if attempts_amount > 0 or element is None:
            print ("Too Many Attempts")
            tb = sys.exc_info()[2]
            raise Exception("TOO MANY ATTEMPTS TO FIND" + search_element).with_traceback(tb)

    @staticmethod
    def get_driver():

        #path_to_chromedriver = r"C:/Users/amac/Documents/Development/Utilities/chromedriver.exe"
        #driver = webdriver.Chrome(executable_path = path_to_chromedriver)

        fp = webdriver.FirefoxProfile()
        path_modify_header = 'modify_headers-0.7.1.1-fx.xpi'
        fp.add_extension(path_modify_header)
        fp.set_preference("modifyheaders.headers.count", 1)
        fp.set_preference("modifyheaders.headers.action0", "Add")
        fp.set_preference("modifyheaders.headers.name0", "nm")
        fp.set_preference("modifyheaders.headers.value0", "vl")
        fp.set_preference("modifyheaders.headers.enabled0", True)
        fp.set_preference("modifyheaders.config.active", True)
        fp.set_preference("modifyheaders.config.alwaysOn", True)
        try:
            driver = webdriver.Firefox(firefox_profile=fp)
        except:
            driver = webdriver.Firefox()

        return driver

    @staticmethod
    def is_element_exists_by_class_name(driver, class_name):
        try:
            driver.find_element_by_class_name(class_name)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def is_element_exists_by_xpath(driver, xpath):
        try:
            driver.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def is_element_exists_by_id(driver, element_id):
        try:
            driver.find_element_by_id(element_id)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def is_element_exists_by_tag_name(driver, tag_name):
        try:
            driver.find_element_by_tag_name(tag_name)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    @timeout(10)
    def click_on_position(driver, element, x, y):
        if element:
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(element, x, y)
            print ("TEST: Clicking")
            sleep(1)
            action.click()
            #print ("Click")
            sleep(1)
            action.perform()
            #print ("Done")
        else:
            print ("Element Not There")

    @staticmethod
    def open_new_tab(driver):
        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')

    @staticmethod
    def has_another_tabs(driver):
        return len(driver.window_handles) > 1

    @staticmethod
    def scroll_page_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    @staticmethod
    def focus_window(driver):
        driver.execute_script("window.focus();")

    @staticmethod
    def close_driver(driver):
        driver.close()
