from utils.selenium_util import SeleniumUtil as SeleniumUtil
from utils.zillow_interface_util import ZillowUtil
from utils.data_util import read_ids_from_csv_file, get_coordinates_from_url, get_coordinate_string_from_url,get_digits_from_string
from utils.ids_storage import DataStorage
from utils.error_formatting import format_exception
from string import Template
from time import sleep

class ParsingController:
    def start(self):
        self.init_ids_storage()
        driver = SeleniumUtil.get_driver()
        driver.get(ZillowUtil.MAIN_PAGE_URL)
        self.init_parsing(driver)

    def init_parsing(self, driver):
        while True:
            if ZillowUtil.SEARCH_HOMES_URL in driver.current_url:
                if ZillowUtil.is_control_button_displayed(driver):
                    if ZillowUtil.is_parsing_start_button_clicked(driver):
                        self.handle_parsing_start(driver)
                else:
                    try:
                        SeleniumUtil.get_element_after_loading(driver, ZillowUtil.SEARCH_MAP_CONTAINER_ID,
                                                               SeleniumUtil.WAIT_ELEMENT_ID_TYPE)
                        ZillowUtil.init_control_button(driver)
                    except Exception as e:
                        print(format_exception())
                        print("Map was not loaded. Trying again", e)

    def handle_parsing_start(self, driver):
        radius_value = ZillowUtil.get_radius_value(driver)
        # noinspection
        current_x_position,current_y_position = ZillowUtil.get_starting_positions(driver)

        if radius_value == 0:
            #ZillowUtil.init_progress_bar(driver,current_x_position,current_y_position)
            ZillowUtil.handle_selected_map_area(driver,current_x_position,current_y_position)
            print("Parsing completed")
            ZillowUtil.init_control_button(driver)
        else:
            areas_urls = self.generate_map_areas_urls(driver, radius_value)
            areas_urls.remove(driver.current_url)
            areas_urls.insert(0, driver.current_url)
            #ZillowUtil.init_progress_bar(driver)
            for current_area_url in areas_urls:
                driver.get(current_area_url)
                #ZillowUtil.init_progress_bar(driver)
                ZillowUtil.handle_selected_map_area(driver,current_x_position,current_y_position)
                print("AREA", current_area_url, " completed")
            print("All selected areas were parsed")
            ZillowUtil.init_control_button(driver)

    def generate_map_areas_urls(self, driver, radius_value):
        coordinates = get_coordinates_from_url(driver.current_url)
        indexes = self.generate_coordinates_indexes(radius_value)
        delta_x = coordinates.get("x1") - coordinates.get("x2")
        delta_y = coordinates.get("y1") - coordinates.get("y2")
        areas_coordinates = self.get_new_areas_coordinates(indexes, coordinates, delta_x, delta_y)
        return self.get_areas_urls(driver, areas_coordinates)

    def get_areas_urls(self, driver, areas_coordinates):
        urls = []
        coordinate_string_in_url = get_coordinate_string_from_url(driver.current_url)
        for area_c in areas_coordinates:
            s = Template('$x1,$y1,$x2,$y2')
            template_coordinates = s.substitute(
                x2=area_c.get("x2"),
                y2=area_c.get("y2"),
                x1=area_c.get("x1"),
                y1=area_c.get("y1")
            )
            urls.append(driver.current_url.replace(coordinate_string_in_url, template_coordinates))
        return urls

    def determine_coordinate_value(self, index_value, coordinate_value, delta):
        if index_value == 0:
            return coordinate_value
        else:
            return coordinate_value + delta * index_value

    def get_new_areas_coordinates(self, indexes, coordinates, delta_x, delta_y):
        areas_coordinates = []
        for index in indexes:
            y = index.get("y")
            x = index.get("x")
            x2_new_value = self.determine_coordinate_value(x, coordinates.get("x2"), delta_x)
            y2_new_value = self.determine_coordinate_value(y, coordinates.get("y2"), delta_y)
            areas_coordinates.append({
                "x2": x2_new_value,
                "y2": y2_new_value,
                "x1": x2_new_value + delta_x,
                "y1": y2_new_value + delta_y
            })
        return areas_coordinates

    def generate_coordinates_indexes(self, radius):
        indexes = []
        first_index = 0 - radius
        while first_index <= radius:
            second_index = 0 - radius
            while second_index <= radius:
                indexes.append({
                    "x": first_index,
                    "y": second_index
                })
                second_index += 1
            first_index += 1
        return indexes

    def init_ids_storage(self):
        try:
            ids = read_ids_from_csv_file()
            DataStorage.getInstance().set_storage(ids)
        except:
            print("Can't read data from data storage")
