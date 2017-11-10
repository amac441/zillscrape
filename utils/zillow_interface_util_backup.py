from utils.selenium_util import SeleniumUtil
from selenium.common.exceptions import NoSuchElementException
from utils.data_util import *
from time import sleep


class ZillowUtil:
    MAIN_PAGE_URL = "https://www.zillow.com/"
    MAIN_PAGE_URL = "https://www.zillow.com/homes/for_sale/globalrelevanceex_sort/41.270589,-95.99901,41.267803,-96.005501_rect/17_zm/"

    SEARCH_MAP_CONTAINER_ID = "searchMap-map-wrapper"
    POINTS_LAYER_CLASS_NAME = "hhLayer"
    SEARCH_HOMES_URL = "homes"
    DESCRIPTION_POP_UP_ID = "detail-container-column"
    REGION_CITY_CONTAINER_ID = "region-city"
    ADDRESS_SPAN_CLASS_NAME = "zsg-breadcrumbs-text"
    ID_DELIMITER = "-"
    SALE_STATUS_DATA_CONTAINER_ID = "home-value-wrapper"
    STATUS_XPATH = '//*[@id="home-value-wrapper"]/div[1]/div[1]'
    AMOUNT_IN_STATUS_DELIMITER = ":"
    FOR_SALE_STATUS_CLASS_NAME = "for-sale-row"
    ZESTIMATE_SIGN_CLASS_NAME = "zsg-tooltip-launch_keyword"
    ZESTIMATE_SIGN_VALUE = "Zestimate"
    ZESTIMATE_ALTERNATIVE_CLASS_NAME = "zestimate"
    DEFAULT_VALUE = "None"
    HEADER_CONTAINER_CLASS_NAME = "zsg-content-header"
    DEFAULT_DESCRIPTION_VALUE = "--"
    BED_ROOMS_SPAN_XPATH = ".//span[2]"
    BATH_ROOMS_SPAN_XPATH = ".//span[4]"
    FOOTAGE_XPATH = ".//span[6]"
    FACTS_CONTAINER_CLASS_NAME = "hdp-facts-expandable-container"
    FACTS_NO_DATA_VALUE = "No Data"
    FACT_ICONS_CLASSES = ["zsg-icon-buildings", "zsg-icon-calendar", "zsg-icon-heat", "zsg-icon-snowflake",
                          "zsg-icon-parking", "zsg-icon-mls"]
    PRICE_HISTORY_ID = 'hdp-price-history'
    PRICE_PATH_IN_CELL = ".//span[1]"
    DEFAULT_PRICE_CHANGE_VALUE = "0%"
    MONTHS_RENT_SUFFIX = "/mo"
    START_EVENT_ID = 1
    LISTING_REMOVED_EVENT_TYPE = "Listing removed"
    PARSING_PROGRESS_ICON_CLASS_NAME = "parsing_progress_icon"
    PARSING_PROGRESS_ID = "parsing_progress_container"
    START_BUTTON_TEMPLATE = '<button id="start_parsing_button" class="z-map-button" style="position:absolute; bottom: 50px; ' \
                            'z-index: 21; right: 7px; width: auto; outline: 0;">' \
                            'Start parsing' \
                            '</button>'

    PROGRESS_BAR_ANIMATION_STYLE = "<style>" \
                                   "@-webkit-keyframes spin {" \
                                   "0% { -webkit-transform: rotate(0deg); }" \
                                   "100% { -webkit-transform: rotate(360deg); }" \
                                   "}" \
                                   "@keyframes spin {" \
                                   "0% { transform: rotate(0deg); }" \
                                   "100% { transform: rotate(360deg); }" \
                                   "}" \
                                   "</style>"

    PROGRESS_BAR_TEMPLATE = '<div id="parsing_progress_container">' + PROGRESS_BAR_ANIMATION_STYLE + \
                            '<div class="parsing_progress_icon" style="border: 16px solid #f3f3f3; ' \
                            'position:absolute; bottom: 50px; z-index: 21; right: 7px; width: auto; outline: 0;' \
                            ' border-radius: 50%; border-top: 16px solid blue; ' \
                            ' border-right: 16px solid green;  border-bottom:' \
                            ' 16px solid red;  width: 60px;  height: 60px;  ' \
                            '-webkit-animation: spin 2s linear infinite;  ' \
                            'animation: spin 2s linear infinite;"></div><div>'

    EXPAND_BUTTON_LINK_XPATH = '//*[@id="hdp-popout-menu"]/a'
    STEP_SIZE_IN_PX = 10
    POP_UP_APPEARING_DELAY_IN_SEC = 1
    CLOSE_POP_UP_BUTTON_CLICK = "hc-back-to-list"
    POP_UP_FOOTER_CLASS_NAME = "zsg-subfooter"
    ADDRESS_LOCALITY_ITEM_PROP = "addressLocality"
    STREET_ADDRESS_ITEM_PROP = "streetAddress"
    HOME_PRESS_AREA_CLASS_NAME = "home-details-price-area"

    @staticmethod
    def wait_for_search_homes_url(driver):
        while ZillowUtil.SEARCH_HOMES_URL not in driver.current_url:
            continue

    @staticmethod
    def parse_home_data(driver):
        sleep(3)
        SeleniumUtil.get_element_after_loading(driver, "search-detail-lightbox_content")
        city = ZillowUtil.get_city_name(driver)
        address = ZillowUtil.get_street_address(driver)
        print("ADRESS_CITY", address, city)
        status_data = ZillowUtil.get_status_data(driver)
        if status_data.get("amount") is not None:
            amount = status_data.get("amount")
        else:
            amount = ZillowUtil.get_amount_for_not_sold_status(driver)

        rooms_amount_data = ZillowUtil.get_rooms_amount(driver)
        home_facts = ZillowUtil.parse_home_facts(driver)

        return {
            "unique_id": ZillowUtil.get_unique_id(city, address),
            "full_address": ZillowUtil.get_full_address(driver),
            "sale_status": status_data.get("status"),
            "amount": amount,
            "zestimate": ZillowUtil.get_zestimate_value(driver),
            "beds": rooms_amount_data.get("beds"),
            "baths": rooms_amount_data.get("baths"),
            "footage": rooms_amount_data.get("footage"),
            "type": home_facts.get("type"),
            "year_built": home_facts.get("year_built"),
            "heating": home_facts.get("heating"),
            "cooling": home_facts.get("cooling"),
            "parking": home_facts.get("parking"),
            "mls": home_facts.get("mls#"),
            "url": ZillowUtil.get_home_url(driver)
        }

    @staticmethod
    def get_full_address(driver):
        if SeleniumUtil.is_element_exists_by_tag_name(driver, "h1"):
            return driver.find_element_by_tag_name("h1").text
        else:
            street_address_element = driver.find_element_by_class_name("hdp-home-header-st-addr")
            city_and_code_element = street_address_element.find_element_by_xpath(".//following-sibling::div")
            return street_address_element.text + " " + city_and_code_element.text

    @staticmethod
    def get_home_url(driver):
        if SeleniumUtil.is_element_exists_by_xpath(driver, ZillowUtil.EXPAND_BUTTON_LINK_XPATH):
            expand_button_link = driver.find_element_by_xpath(ZillowUtil.EXPAND_BUTTON_LINK_XPATH)
            expand_button_link_href = expand_button_link.get_attribute("href")
            return expand_button_link_href[:expand_button_link_href.index("?")]
        else:
            popup_footer = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.POP_UP_FOOTER_CLASS_NAME,
                                                                  SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)

            address_span_container = ZillowUtil.get_span_by_itemprop(popup_footer, "address")
            link_to_expand_information = address_span_container.find_element_by_tag_name("a")
            return ZillowUtil.MAIN_PAGE_URL + link_to_expand_information.get_attribute("href")

    @staticmethod
    def get_city_name(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, ZillowUtil.REGION_CITY_CONTAINER_ID):
            city_container = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.REGION_CITY_CONTAINER_ID)
            return city_container.find_element_by_tag_name('a').text
        else:
            popup_footer = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.POP_UP_FOOTER_CLASS_NAME,
                                                                  SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)
            return ZillowUtil.get_span_value_by_itemprop(popup_footer, ZillowUtil.ADDRESS_LOCALITY_ITEM_PROP)

    @staticmethod
    def get_street_address(driver):
        if SeleniumUtil.is_element_exists_by_class_name(driver, ZillowUtil.ADDRESS_SPAN_CLASS_NAME):
            return driver.find_element_by_class_name(ZillowUtil.ADDRESS_SPAN_CLASS_NAME).text
        else:
            popup_footer = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.POP_UP_FOOTER_CLASS_NAME,
                                                                  SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)
            return ZillowUtil.get_span_value_by_itemprop(popup_footer, ZillowUtil.STREET_ADDRESS_ITEM_PROP)

    @staticmethod
    def get_unique_id(city, address):
        return address.replace(" ", ZillowUtil.ID_DELIMITER) + ZillowUtil.ID_DELIMITER \
               + city.replace(" ", ZillowUtil.ID_DELIMITER)

    @staticmethod
    def get_amount_for_not_sold_status(driver):
        if SeleniumUtil.is_element_exists_by_class_name(driver, ZillowUtil.FOR_SALE_STATUS_CLASS_NAME):
            status_container = driver.find_element_by_class_name(ZillowUtil.FOR_SALE_STATUS_CLASS_NAME)
            amount_element = status_container.find_element_by_xpath(".//following-sibling::div")
            return remove_dollar_sign(amount_element.text)
        else:
            return 0

    @staticmethod
    def get_span_value_by_itemprop(driver, itemprop_value):
        span_element = ZillowUtil.get_span_by_itemprop(driver, itemprop_value)
        if span_element is not None:
            return span_element.text
        return None

    @staticmethod
    def get_span_by_itemprop(driver, itemprop_value):
        span_elements = driver.find_elements_by_tag_name("span")
        for span_element in span_elements:
            if span_element.get_attribute("itemprop") == itemprop_value:
                return span_element
        return None

    @staticmethod
    def get_status_data(driver):
        status_data = {}
        if SeleniumUtil.is_element_exists_by_xpath(driver, ZillowUtil.STATUS_XPATH):
            status_element = driver.find_element_by_xpath(ZillowUtil.STATUS_XPATH)
        else:
            status_parent = driver.find_element_by_class_name(ZillowUtil.HOME_PRESS_AREA_CLASS_NAME)
            status_container = status_parent.find_element_by_class_name("status")
            status_element = status_container.find_element_by_class_name("zsg-tooltip-launch_keyword")

        status_text = status_element.text
        if ZillowUtil.AMOUNT_IN_STATUS_DELIMITER in status_text:
            status_parts = status_text.split(ZillowUtil.AMOUNT_IN_STATUS_DELIMITER)
            status_data["amount"] = remove_dollar_sign(status_parts[1])
            status_data["status"] = status_parts[0]
        else:
            status_data["status"] = status_text

        return status_data

    @staticmethod
    def get_zestimate_value(driver):
        if SeleniumUtil.is_element_exists_by_class_name(driver, ZillowUtil.ZESTIMATE_ALTERNATIVE_CLASS_NAME)\
                and not SeleniumUtil.is_element_exists_by_id(driver, ZillowUtil.SALE_STATUS_DATA_CONTAINER_ID):
            zestimate_container = driver.find_element_by_class_name(ZillowUtil.ZESTIMATE_ALTERNATIVE_CLASS_NAME)
            zestimate_sign_span = zestimate_container.find_element_by_class_name(
                ZillowUtil.ZESTIMATE_SIGN_CLASS_NAME)

            return zestimate_container.text.replace(zestimate_sign_span.text + ":", "").strip()
        elif SeleniumUtil.is_element_exists_by_class_name(driver, ZillowUtil.ZESTIMATE_SIGN_CLASS_NAME):
            return ZillowUtil.get_zestimate_value_from_container(driver)
        return ZillowUtil.DEFAULT_VALUE

    @staticmethod
    def get_zestimate_value_from_container(container):
        zestimate_sign_span = container.find_element_by_class_name(ZillowUtil.ZESTIMATE_SIGN_CLASS_NAME)
        if ZillowUtil.ZESTIMATE_SIGN_VALUE in zestimate_sign_span.text:
            zestimate_text = zestimate_sign_span.find_element_by_xpath(".//following-sibling::span").text
            if DOLLAR_SIGN in zestimate_text:
                zestimate_text = remove_dollar_sign(zestimate_text)
            return zestimate_text
        return ZillowUtil.DEFAULT_VALUE

    @staticmethod
    def get_rooms_amount(driver):
        rooms_description = {}
        if SeleniumUtil.is_element_exists_by_class_name(driver, ZillowUtil.HEADER_CONTAINER_CLASS_NAME):
            header_container = driver.find_element_by_class_name(ZillowUtil.HEADER_CONTAINER_CLASS_NAME)
            short_description = header_container.find_element_by_tag_name("h3")
        else:
            short_description = driver.find_element_by_class_name("edit-facts-light")

        if SeleniumUtil.is_element_exists_by_xpath(short_description, ZillowUtil.BED_ROOMS_SPAN_XPATH):
            bed_rooms_span = short_description.find_element_by_xpath(ZillowUtil.BED_ROOMS_SPAN_XPATH)
            rooms_description["beds"] = ZillowUtil.parse_rooms_amount_from_string(bed_rooms_span.text)
        if SeleniumUtil.is_element_exists_by_xpath(short_description, ZillowUtil.BATH_ROOMS_SPAN_XPATH):
            bath_rooms_span = short_description.find_element_by_xpath(ZillowUtil.BATH_ROOMS_SPAN_XPATH)
            rooms_description["baths"] = ZillowUtil.parse_rooms_amount_from_string(bath_rooms_span.text)
        if SeleniumUtil.is_element_exists_by_xpath(short_description, ZillowUtil.FOOTAGE_XPATH):
            footage_span = short_description.find_element_by_xpath(ZillowUtil.FOOTAGE_XPATH)
            rooms_description["footage"] = ZillowUtil.parse_footage_from_string(footage_span.text)
        return rooms_description

    @staticmethod
    def parse_rooms_amount_from_string(inform_str):
        if ZillowUtil.DEFAULT_DESCRIPTION_VALUE not in inform_str:
            digits = get_digits_from_string(inform_str)
            if digits is None:
                return ZillowUtil.DEFAULT_DESCRIPTION_VALUE
            else:
                return digits
        return ZillowUtil.DEFAULT_DESCRIPTION_VALUE

    @staticmethod
    def parse_footage_from_string(inform_str):
        if ZillowUtil.DEFAULT_DESCRIPTION_VALUE not in inform_str:
            return inform_str[:inform_str.rindex(" ")]
        return ZillowUtil.DEFAULT_DESCRIPTION_VALUE

    @staticmethod
    def parse_home_facts(driver):
        facts = {}
        if SeleniumUtil.is_element_exists_by_class_name(driver, ZillowUtil.FACTS_CONTAINER_CLASS_NAME):
            facts_container = driver.find_element_by_class_name(ZillowUtil.FACTS_CONTAINER_CLASS_NAME)
            top_facts_container = facts_container.find_element_by_class_name("zsg-g_gutterless")
            top_facts = top_facts_container.find_elements_by_xpath("./div")
            for fact in top_facts:
                for icon_class in ZillowUtil.FACT_ICONS_CLASSES:
                    if SeleniumUtil.is_element_exists_by_class_name(fact, icon_class):
                        fact_name = fact.find_element_by_class_name("hdp-fact-ataglance-heading").text.replace(" ", "_")
                        value = fact.find_element_by_class_name("hdp-fact-ataglance-value").text
                        if value.lower() == ZillowUtil.FACTS_NO_DATA_VALUE.lower():
                            value = None
                        facts[fact_name.lower()] = value
        return facts

    @staticmethod
    def parse_price_history(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, ZillowUtil.PRICE_HISTORY_ID):
            price_history_container = driver.find_element_by_id(ZillowUtil.PRICE_HISTORY_ID)

            if SeleniumUtil.is_element_exists_by_id(driver, "tax-price-history"):
                collapsible_container = driver.find_element_by_xpath('//div[@id="tax-price-history"]/parent::section')
            else:
                collapsible_container = price_history_container.find_element_by_xpath('..')
            collapsible_container.click()

            tbody = SeleniumUtil.get_element_after_loading(price_history_container, "tbody",
                                                           SeleniumUtil.WAIT_ELEMENT_TAG_NAME_TYPE)
            if ZillowUtil.is_price_history_filled(tbody):
                rows = tbody.find_elements_by_tag_name("tr")
                price_history_data = []
                event_id = ZillowUtil.START_EVENT_ID
                for row in rows:
                    row_cells = row.find_elements_by_tag_name("td")
                    price_history_data.append({
                        "id": event_id,
                        "event_date": row_cells[0].text,
                        "event": row_cells[1].text,
                        "price": ZillowUtil.get_history_price_from_cell(row_cells[2]),
                        "price_change": ZillowUtil.get_history_price_change_from_cell(row_cells[2]),
                        "agents": ZillowUtil.get_agents_name(driver, row_cells),
                        "rental": ZillowUtil.check_home_rental_for_event(row_cells[2]),
                        "listing_removed": ZillowUtil.check_listing_removed(event_id, row_cells[2], row_cells[1].text)
                    })
                    event_id += 1
                return price_history_data
        return None

    @staticmethod
    def get_agents_name(driver, row_cells):
        if SeleniumUtil.is_element_exists_by_id(driver, "tax-price-history"):
            return row_cells[3].text
        else:
            return row_cells[4].text

    @staticmethod
    def check_listing_removed(event_id, price_cell, event_type):
        if event_id == ZillowUtil.START_EVENT_ID and not ZillowUtil.check_home_rental_for_event(
                price_cell) and event_type == ZillowUtil.LISTING_REMOVED_EVENT_TYPE:
            return True
        return False

    @staticmethod
    def check_home_rental_for_event(price_cell):
        if ZillowUtil.MONTHS_RENT_SUFFIX in price_cell.find_element_by_xpath(ZillowUtil.PRICE_PATH_IN_CELL).text:
            return True
        return False

    @staticmethod
    def get_history_price_from_cell(cell):
        price_cell_text = cell.find_element_by_xpath(ZillowUtil.PRICE_PATH_IN_CELL).text
        if "/" in price_cell_text:
            price_cell_text = price_cell_text[:price_cell_text.index("/")]
        return remove_dollar_sign(price_cell_text)

    @staticmethod
    def get_history_price_change_from_cell(cell):
        if SeleniumUtil.is_element_exists_by_class_name(cell, "delta-value"):
            delta_price_container = cell.find_element_by_class_name("delta-value")
            if SeleniumUtil.is_element_exists_by_tag_name(delta_price_container, "span"):
                return delta_price_container.find_element_by_tag_name("span").text
        return ZillowUtil.DEFAULT_PRICE_CHANGE_VALUE

    @staticmethod
    def is_price_history_filled(tbody):
        if SeleniumUtil.is_element_exists_by_tag_name(tbody, "tr"):
            if len(tbody.find_elements_by_tag_name("tr")) == 1:
                tr_element = tbody.find_element_by_tag_name("tr")
                if len(tr_element.find_elements_by_tag_name("td")) == 1:
                    return False
            return True
        return False

    @staticmethod
    def init_control_button(driver):
        control_button = driver.find_element_by_id("map-list-ratio-toggle")
        if SeleniumUtil.is_element_exists_by_id(driver, ZillowUtil.PARSING_PROGRESS_ID):
            parsing_progress_container = driver.find_element_by_id(ZillowUtil.PARSING_PROGRESS_ID)
            driver.execute_script("arguments[0].outerHTML = '" + ZillowUtil.START_BUTTON_TEMPLATE + "';",
                                  parsing_progress_container)
        else:
            outer_html_width_button = control_button.get_attribute("outerHTML") + ZillowUtil.START_BUTTON_TEMPLATE
            driver.execute_script("arguments[0].outerHTML = '" + outer_html_width_button + "';", control_button)
        start_parsing_button = SeleniumUtil.get_element_after_loading(driver, "start_parsing_button")
        driver.execute_script("""\
          arguments[0].addEventListener("click", handle_start_button_click);

          function handle_start_button_click() {
              console.log("CLICK START BUTTON");
              this.classList.add('start_parsing_launched');
              this.removeEventListener('click', handle_start_button_click)
          }
          """, start_parsing_button)

    @staticmethod
    def wait_for_parsing_start_click(driver, start_handler):
        while not SeleniumUtil.is_element_exists_by_class_name(driver, "start_parsing_launched"):
            sleep(1)
        start_handler(driver)

    @staticmethod
    def replace_start_parsing_button_on_progress_bar(driver):
        start_parsing_button = SeleniumUtil.get_element_after_loading(driver, "start_parsing_button")
        driver.execute_script("arguments[0].outerHTML = '" + ZillowUtil.PROGRESS_BAR_TEMPLATE + "';",
                              start_parsing_button)

    @staticmethod
    def handle_selected_map_area(driver):
        homes_data = []
        map_container = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.SEARCH_MAP_CONTAINER_ID)
        points_layer = SeleniumUtil.get_element_after_loading(map_container, ZillowUtil.POINTS_LAYER_CLASS_NAME,
                                                              SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)
        width = get_digits_from_string(points_layer.value_of_css_property("width"))
        height = get_digits_from_string(points_layer.value_of_css_property("height"))
        current_x_position = width
        current_y_position = height
        start_url = driver.current_url
        while current_y_position > 0:
            current_y_position -= ZillowUtil.STEP_SIZE_IN_PX
            while current_x_position > 0:
                current_x_position -= ZillowUtil.STEP_SIZE_IN_PX
                SeleniumUtil.click_on_position(driver, points_layer, current_x_position, current_y_position)
                sleep(ZillowUtil.POP_UP_APPEARING_DELAY_IN_SEC)
                if start_url != driver.current_url and ZillowUtil.is_content_pop_up_displayed(driver):
                    print(ZillowUtil.parse_home_data(driver))
                    driver.find_element_by_class_name(ZillowUtil.CLOSE_POP_UP_BUTTON_CLICK).click()
                else:
                    print(current_x_position, "doesn't have houses")

    @staticmethod
    def is_content_pop_up_displayed(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, "search-detail-lightbox"):
            search_detail_lightbox = driver.find_element_by_id("search-detail-lightbox")
            classes = search_detail_lightbox.get_attribute("class")
            if "yui3-lightbox-focused" in classes:
                return True
        return False
