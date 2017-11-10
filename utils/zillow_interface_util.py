from utils.selenium_util import SeleniumUtil
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from utils.data_util import remove_dollar_sign, get_digits_from_string, write_home_data, isInt
from time import sleep
from utils.ids_storage import DataStorage
from utils.error_formatting import format_exception

                            # '<div id="start_button_container"> <div id="data_input" class="z-map-button" style="position:absolute; bottom: 80px; z-index: 21; right: 7px; width: 50px; outline: 0;">' \
                            # '<input id="parsing_radius" name="someid" maxlength="1" value="0" type="number"' \
                            # 'onkeypress="return (event.which >= 48 && event.which <= 57) || event.which == 8 || event.which == 46 || event.which == 37 || event.which == 39;">' \
                            # '</div>'\
                            # '<button id="start_parsing_button" class="z-map-button" style="position:absolute; bottom: 50px; ' \
                            # 'z-index: 21; right: 7px; width: auto; outline: 0;">' \
                            # 'Start parsing' \
                            # '</button></div>'

class ZillowUtil:
    MAIN_PAGE_URL = "https://www.zillow.com/"
    MAIN_PAGE_URL = "https://www.zillow.com/homes/for_sale/globalrelevanceex_sort/41.270589,-95.99901,41.267803,-96.005501_rect/17_zm/"
    MAIN_PAGE_URL = "https://www.zillow.com/homes/for_sale/globalrelevanceex_sort/38.651573,-90.290304,38.648678,-90.296794_rect/17_zm/"
    # MAIN_PAGE_URL = "https://www.zillow.com/homes/for_sale/globalrelevanceex_sort/38.651566,-90.290304,38.648672,-90.296795_rect/17_zm/
    SEARCH_MAP_CONTAINER_ID = "searchMap-map-wrapper"
    POINTS_LAYER_CLASS_NAME = "hhLayer"
    SEARCH_HOMES_URL = "homes"
    DESCRIPTION_POP_UP_ID = "detail-container-column"
    REGION_CITY_CONTAINER_ID = "region-city"
    ADDRESS_SPAN_CLASS_NAME = "zsg-breadcrumbs-text"
    ID_DELIMITER = "-"
    SALE_STATUS_DATA_CONTAINER_ID = "home-value-wrapper"
    STATUS_XPATH = '//*[@id="home-value-wrapper"]/div[1]/div[1]'
    HOME_VALUES_DIVS_XPATH = '//*[@id="home-value-wrapper"]/div[1]/div'
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
    START_BUTTON_CONTAINER_TEMPLATE = \
                            '<div id="start_button_container"> <div id="data_input" class="z-map-button" style="position:absolute; bottom: 80px; z-index: 21; right: 7px; width: 50px; outline: 0;">' \
                            '<input id="x_start" name="someid" maxlength="4" value="0" type="number"' \
                            'onkeypress="return (event.which &gt;= 48 &amp;&amp; event.which &lt;= 57) || event.which == 8 || event.which == 46 || event.which == 37 || event.which == 39;" />' \
                            '<input id="y_start" name="someid" maxlength="4" value="0" type="number"' \
                            'onkeypress="return (event.which &gt;= 48 &amp;&amp; event.which &lt;= 57) || event.which == 8 || event.which == 46 || event.which == 37 || event.which == 39;"/>' \
                            '<input id="parsing_radius" name="someid" maxlength="1" value="0" type="number"' \
                            'onkeypress="return (event.which >= 48 && event.which <= 57) || event.which == 8 || event.which == 46 || event.which == 37 || event.which == 39;"></div>' \
                            '<button id="start_parsing_button" class="z-map-button" style="position:absolute; bottom: 50px; z-index: 21; right: 7px; width: auto; outline: 0;">' \
                            'Start parsing</button></div>'


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
    POP_UP_APPEARING_DELAY_IN_SEC = 4
    CLOSE_POP_UP_BUTTON_CLICK = "hc-back-to-list"
    POP_UP_FOOTER_CLASS_NAME = "zsg-subfooter"
    ADDRESS_LOCALITY_ITEM_PROP = "addressLocality"
    STREET_ADDRESS_ITEM_PROP = "streetAddress"
    HOME_PRESS_AREA_CLASS_NAME = "home-details-price-area"
    DEFAULT_RADIUS_VALUE = 0

    @staticmethod
    def wait_for_search_homes_url(driver):
        while ZillowUtil.SEARCH_HOMES_URL not in driver.current_url:
            continue

    @staticmethod
    def parse_home_data(driver):

        SeleniumUtil.get_element_after_loading(driver, "zsg-subfooter-content", SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)
        print("TEST: getting city")
        city = ZillowUtil.get_city_name(driver)
        address = ZillowUtil.get_street_address(driver)
        status_data = ZillowUtil.get_status_data(driver)

        if status_data.get("amount") is not None:
            amount = status_data.get("amount")
        else:
            amount = ZillowUtil.get_amount_for_not_sold_status(driver)

        home_parameters = ZillowUtil.get_home_parameters(driver)
        home_facts = ZillowUtil.parse_home_facts(driver)

        return {
            "unique_id": ZillowUtil.get_unique_id(city, address),
            "full_address": ZillowUtil.get_full_address(driver),
            "sale_status": status_data.get("status"),
            "amount": amount,
            "zestimate": ZillowUtil.get_zestimate_value(driver),
            "beds": home_parameters.get("beds"),
            "baths": home_parameters.get("baths"),
            "footage": home_parameters.get("footage"),
            "type": home_facts.get("type"),
            "year_built": home_facts.get("year_built"),
            "heating": home_facts.get("heating"),
            "cooling": home_facts.get("cooling"),
            "parking": home_facts.get("parking"),
            "mls": home_facts.get("mls#"),
            "url": ZillowUtil.get_url(driver),
            "price_history": ZillowUtil.parse_price_history(driver)
        }

    @staticmethod
    def get_full_address(driver):
        return " ".join(driver.find_element_by_tag_name("h1").text.splitlines())

    @staticmethod
    def get_url(driver):
        return driver.current_url[:driver.current_url.index("?")]

    @staticmethod
    def get_full_page_url(driver):
        SeleniumUtil.get_element_after_loading(driver, "zsg-subfooter-content", SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)
        if SeleniumUtil.is_element_exists_by_xpath(driver, ZillowUtil.EXPAND_BUTTON_LINK_XPATH):
            expand_button_link = driver.find_element_by_xpath(ZillowUtil.EXPAND_BUTTON_LINK_XPATH)
            expand_button_link_href = expand_button_link.get_attribute("href")
            return expand_button_link_href
        else:
            expand_button_link_container = SeleniumUtil.get_element_after_loading(driver, "hdp-popout-menu",
                                                                                  SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)
            expand_button_link = expand_button_link_container.find_element_by_tag_name("a")
            if ZillowUtil.MAIN_PAGE_URL in expand_button_link.get_attribute("href"):
                return expand_button_link.get_attribute("href")
            return ZillowUtil.MAIN_PAGE_URL + expand_button_link.get_attribute("href")

    @staticmethod
    def get_city_name(driver):
        city_container = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.REGION_CITY_CONTAINER_ID)
        return city_container.find_element_by_tag_name('a').text

    @staticmethod
    def get_street_address(driver):
        return driver.find_element_by_class_name(ZillowUtil.ADDRESS_SPAN_CLASS_NAME).text

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
        status_element = driver.find_element_by_xpath(ZillowUtil.STATUS_XPATH)
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
        home_values_elements = driver.find_elements_by_xpath(ZillowUtil.HOME_VALUES_DIVS_XPATH)
        for value_element in home_values_elements:
            span_elements = value_element.find_elements_by_tag_name("span")
            for span in span_elements:
                if span.text.lower().startswith("zestimate") and span.get_attribute("data-target-id") == "zest-tip-hdp":
                    zestimate_with_dollar_sign = span.find_element_by_xpath(".//following-sibling::span").text
                    return remove_dollar_sign(zestimate_with_dollar_sign)
        return ZillowUtil.DEFAULT_VALUE

    @staticmethod
    def get_home_parameters(driver):
        rooms_description = {}

        header_container = driver.find_element_by_class_name(ZillowUtil.HEADER_CONTAINER_CLASS_NAME)
        short_description = header_container.find_element_by_tag_name("h3")

        if SeleniumUtil.is_element_exists_by_xpath(short_description, ZillowUtil.BED_ROOMS_SPAN_XPATH):
            bed_rooms_span = short_description.find_element_by_xpath(ZillowUtil.BED_ROOMS_SPAN_XPATH)
            rooms_description["beds"] = ZillowUtil.parse_home_property_value_from_string(bed_rooms_span.text)
        if SeleniumUtil.is_element_exists_by_xpath(short_description, ZillowUtil.BATH_ROOMS_SPAN_XPATH):
            bath_rooms_span = short_description.find_element_by_xpath(ZillowUtil.BATH_ROOMS_SPAN_XPATH)
            rooms_description["baths"] = ZillowUtil.parse_home_property_value_from_string(bath_rooms_span.text)
        if SeleniumUtil.is_element_exists_by_xpath(short_description, ZillowUtil.FOOTAGE_XPATH):
            footage_span = short_description.find_element_by_xpath(ZillowUtil.FOOTAGE_XPATH)
            rooms_description["footage"] = ZillowUtil.parse_home_property_value_from_string(footage_span.text)
        return rooms_description

    @staticmethod
    def parse_home_property_value_from_string(inform_str):
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
            tbody = SeleniumUtil.get_element_after_loading(price_history_container, "tbody",
                                                           SeleniumUtil.WAIT_ELEMENT_TAG_NAME_TYPE)

            if ZillowUtil.is_price_history_filled(tbody):
                ZillowUtil.maximize_price_history_display(price_history_container, tbody)
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
                    "agents": ZillowUtil.get_agents_name(price_history_container, row_cells),
                    "rental": ZillowUtil.check_home_rental_for_event(row_cells[2]),
                    "listing_removed": ZillowUtil.check_listing_removed(event_id, row_cells[2], row_cells[1].text)
                    })
                    event_id += 1
                return price_history_data
        return None

    @staticmethod
    def maximize_price_history_display(price_history_container, tbody):
        if ZillowUtil.is_price_history_minimized(price_history_container, tbody):
            table_footer = price_history_container.find_element_by_tag_name("tfoot")
            table_footer.find_element_by_tag_name("a").click()

    @staticmethod
    def is_price_history_minimized(price_history_container, tbody):
        table_element = price_history_container.find_element_by_tag_name("table")
        return "yui3-toggle-content-minimized" in table_element.get_attribute("class") and \
               SeleniumUtil.is_element_exists_by_class_name(tbody, "minimize")

    @staticmethod
    def get_agents_name(driver, row_cells):
        if SeleniumUtil.is_element_exists_by_class_name(driver, "ph-agents"):
            return row_cells[3].text
        else:
            return ""

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
    def is_control_button_displayed(driver):
        return SeleniumUtil.is_element_exists_by_id(driver, "start_parsing_button")

    @staticmethod
    def get_radius_value(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, "parsing_radius"):
            radius_input_field_value = driver.find_element_by_id("parsing_radius").get_attribute("value")
            if radius_input_field_value != "" and isInt(radius_input_field_value):
                return int(radius_input_field_value)
        return ZillowUtil.DEFAULT_RADIUS_VALUE

    @staticmethod
    def get_starting_positions(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, "x_start"):
            x_val_element = driver.find_element_by_id("x_start").get_attribute("value")
            x_val = int(x_val_element)
        else:
            x_val=0

        if SeleniumUtil.is_element_exists_by_id(driver, "y_start"):
            y_val_element = driver.find_element_by_id("y_start").get_attribute("value")
            y_val = int(y_val_element)
        else:
            y_val=0

        return x_val,y_val

    @staticmethod
    def init_control_button(driver):
        control_button = driver.find_element_by_id("disabled-map-cover")
        if SeleniumUtil.is_element_exists_by_id(driver, ZillowUtil.PARSING_PROGRESS_ID):
            parsing_progress_container = driver.find_element_by_id(ZillowUtil.PARSING_PROGRESS_ID)
            driver.execute_script("arguments[0].outerHTML = '" + ZillowUtil.START_BUTTON_CONTAINER_TEMPLATE + "';",
                                  parsing_progress_container)
        else:
            outer_html = control_button.get_attribute("outerHTML") + ZillowUtil.START_BUTTON_CONTAINER_TEMPLATE
            driver.execute_script("arguments[0].outerHTML = '" + outer_html + "';", control_button)
        start_parsing_button = SeleniumUtil.get_element_after_loading(driver, "start_parsing_button")
        driver.execute_script("""\
          arguments[0].addEventListener("click", handle_start_button_click);

          function handle_start_button_click() {
              if (window.location.href.indexOf("_zm") > 0) {
                  this.classList.add('start_parsing_launched');
                  this.removeEventListener('click', handle_start_button_click)
              }
          }
          """, start_parsing_button)

    @staticmethod
    def is_parsing_start_button_clicked(driver):
        return SeleniumUtil.is_element_exists_by_class_name(driver, "start_parsing_launched")

    @staticmethod
    def init_progress_bar(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, "start_button_container"):
            start_parsing_button = SeleniumUtil.get_element_after_loading(driver, "start_button_container")
            driver.execute_script("arguments[0].outerHTML = '" + ZillowUtil.PROGRESS_BAR_TEMPLATE + "';",
                                  start_parsing_button)
        else:
            control_button = driver.find_element_by_id("disabled-map-cover")
            outer_html_width_progress_bar = control_button.get_attribute("outerHTML") + ZillowUtil.PROGRESS_BAR_TEMPLATE
            driver.execute_script("arguments[0].outerHTML = '" + outer_html_width_progress_bar + "';", control_button)

    @staticmethod
    def handle_selected_map_area(driver, current_x_position, current_y_position):
        map_area_urls = []
        start_url = driver.current_url
        full_page_window = SeleniumUtil.get_driver()

        points_layer = ZillowUtil.get_map_points_layer(driver)
        width = get_digits_from_string(points_layer.value_of_css_property("width"))
        height = get_digits_from_string(points_layer.value_of_css_property("height"))

        if current_y_position == 0:
            current_y_position = height - ZillowUtil.STEP_SIZE_IN_PX


        while current_y_position > 0:

            if current_x_position == 0 or current_x_position < 0:
                current_x_position = width - ZillowUtil.STEP_SIZE_IN_PX

            try:
                while current_x_position > 0:
                    #print ("While")
                    starturlList=list(start_url)
                    intersect=len([i for i,j in zip(starturlList,list(driver.current_url)) if i==j])
                    if intersect/len(starturlList) < .85:
                    #if str(start_url) != str(driver.current_url):
                        driver.get(start_url)
                        points_layer = ZillowUtil.get_map_points_layer(driver)

                    SeleniumUtil.click_on_position(driver, points_layer, current_x_position, current_y_position)
                    print ("TEST: Clicked")
                    sleep(ZillowUtil.POP_UP_APPEARING_DELAY_IN_SEC)

                    if start_url != driver.current_url and ZillowUtil.is_content_pop_up_displayed(driver):
                        #print ("Opened")

                        # if we have not scraped this property yet
                        if driver.current_url not in map_area_urls:
                            home_full_page_url = ZillowUtil.get_full_page_url(driver)

                            #get data
                            ZillowUtil.handle_full_data_page(full_page_window, home_full_page_url)
                            map_area_urls.append(driver.current_url)
                        try:
                            closeElement = driver.find_element_by_class_name(ZillowUtil.CLOSE_POP_UP_BUTTON_CLICK)

                        except:
                            print("Test: closeElement Except")
                            driver.get(start_url)
                            points_layer = ZillowUtil.get_map_points_layer(driver)

                        if closeElement:
                            try:
                                closeElement.click()
                            except:
                                print("Test: no closeElement.click()")

                                driver.get(start_url)
                                points_layer = ZillowUtil.get_map_points_layer(driver)
                            #print ("Closed")
                        else:
                            driver.get(start_url)
                            points_layer = ZillowUtil.get_map_points_layer(driver)
                            print ("Refreshed")
                    else:
                        print("x:", current_x_position, "y: ", current_y_position, "doesn't have homes")

                    current_x_position -= ZillowUtil.STEP_SIZE_IN_PX

                    print("Increment x:", current_x_position, "y: ", current_y_position)

                current_y_position -= ZillowUtil.STEP_SIZE_IN_PX

            except StaleElementReferenceException:
                print("The page was realoded. Updating link to points layer")
                #ZillowUtil.init_progress_bar(driver)
                #refresh URL
                driver.get(start_url)
                points_layer = ZillowUtil.get_map_points_layer(driver)
        SeleniumUtil.close_driver(full_page_window)

    @staticmethod
    def get_map_points_layer(driver):
        map_container = SeleniumUtil.get_element_after_loading(driver, ZillowUtil.SEARCH_MAP_CONTAINER_ID)
        return SeleniumUtil.get_element_after_loading(map_container, ZillowUtil.POINTS_LAYER_CLASS_NAME,
                                                      SeleniumUtil.WAIT_ELEMENT_CLASS_TYPE)

    @staticmethod
    def handle_full_data_page(driver, full_data_page_url):
        try:
            driver.get(full_data_page_url)
            sleep(ZillowUtil.POP_UP_APPEARING_DELAY_IN_SEC)
            SeleniumUtil.scroll_page_down(driver)

            # if SeleniumUtil.is_element_exists_by_id(driver,"search-detail-lightbox_content")

            if ZillowUtil.is_content_pop_up_displayed(driver):
                print ("Test: Full Page Popup")
            else:
                ZillowUtil.save_home_data_to_file(ZillowUtil.parse_home_data(driver))

        except NoSuchElementException as e:
            print("Can't parse url ", full_data_page_url)
            print(e, "\n", format_exception())

    @staticmethod
    def is_content_pop_up_displayed(driver):
        if SeleniumUtil.is_element_exists_by_id(driver, "search-detail-lightbox"):
            search_detail_lightbox = driver.find_element_by_id("search-detail-lightbox")
            classes = search_detail_lightbox.get_attribute("class")
            if "yui3-lightbox-focused" in classes:
                return True
        return False

    @staticmethod
    def save_home_data_to_file(data):
        try:
            write_home_data(data)
            DataStorage.getInstance().add(data.get("unique_id"))
            print("Saved data of home with id", data.get("unique_id"))
        except:
            print("Can't save data to file about ", data.get("unique_id"))
