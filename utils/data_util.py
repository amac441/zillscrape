import csv
import os.path
from utils.ids_storage import DataStorage
import time

DOLLAR_SIGN = "$"
CSV_FILE_FIELDS_DELIMITER = ";"
CSV_FILE_HEADER = [
    "Unique Property ID", "Full Address", "Sale Status", "Amount", "Zestimate", "Beds", "Baths", "Type",
    "Year Built", " Heating", "Cooling", "Parking", "MLS#", "Flooring Square Footage", "URL", "EventID", "Event",
    "Date", "Event", "Price", "Price Change", "Agents", "Rental", "Listing Removed"
]
CSV_FILE_HEADER = [
    "unique_id", "full_address", "sale_status", "amount", "zestimate", "beds", "baths", "footage",
    "type", "year_built", "heating", "cooling", "parking", "mls", "url"
]

CSV_EVENT_HEADER = [
    "id", "event_date", "event", "price", "price_change", "agents", "rental", "listing_removed"
]

ts = time.time()

def isFloat(value):
    try:
        float(value)
        return True
    except:
        return False


def isInt(value):
    try:
        int(value)
        return True
    except:
        return False


def remove_dollar_sign(amount_string):
    return amount_string.replace(DOLLAR_SIGN, "")


def get_digits_from_string(string):
    number_string = ""
    if isInt(string):
        return int(string)
    if len(string.split()) == 1:
        symbols = list(string)
    else:
        symbols = string.split()

    for s in symbols:
        if s.isdigit():
            number_string += s

    if len(number_string) > 0:
        return int(number_string)
    else:
        return None


def get_float_string_from_string(string):
    number_string = ""
    string = string.replace(",", ".")
    if isFloat(string):
        return string

    for s in string.split():
        if isFloat(s):
            number_string = s
    if len(number_string) > 0:
        return number_string
    else:
        return None


def write_to_csv_file(data, file_name="result_%s.csv"%ts):
    is_file_exists = os.path.exists(file_name)
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=CSV_FILE_FIELDS_DELIMITER)
        if not is_file_exists or os.stat(file_name).st_size == 0:
            writer.writerow(CSV_FILE_HEADER+CSV_EVENT_HEADER)
        # datalist = [data[d] for d in CSV_FILE_HEADER]
        writer.writerow(data)

def read_ids_from_csv_file(file_name="result.csv"):
    ids_dict = {}
    if os.path.exists(file_name):
        with open(file_name, newline='') as csvfile:
            data_reader = csv.reader(csvfile, delimiter=CSV_FILE_FIELDS_DELIMITER)
            header_string = ', '.join(CSV_FILE_HEADER+CSV_EVENT_HEADER)
            header_read = False
            for row in data_reader:
                if not header_read and header_string == ', '.join(row):
                    header_read = True
                else:
                    ids_dict[row[0]] = row[0]
    return ids_dict


def write_home_data(data):
    if data is not None and DataStorage.getInstance().is_home_added(data.get("unique_id")):
        if data.get("price_history") is None:
            data_array = []
            empty_price_history_data = [None] * 8
            for key in CSV_FILE_HEADER:   #was key in data
                if data.get(key) is None and key != "price_history":
                    data_array.append("None")
                else:
                    data_array.append(data.get(key))
            data_array.extend(empty_price_history_data)
            write_to_csv_file(data_array)
        else:
            price_history = data.get("price_history")
            rows = []
            for current_price_history in price_history:
                data_row = []
                for key in CSV_FILE_HEADER: #was key in data
                    if key != "price_history":
                        if data.get(key) is None:
                            data_row.append("None")
                        else:
                            data_row.append(data.get(key))
                for price_history_field in CSV_EVENT_HEADER: # was current_price_history:
                    data_row.append(current_price_history.get(price_history_field))
                rows.append(data_row)
            for row in rows:
                write_to_csv_file(row)


def get_coordinates_from_url(url):
    coordinates_string = get_coordinate_string_from_url(url)
    coordinates = coordinates_string.split(",")
    return {
        "x1": float(coordinates[0]),
        "y1": float(coordinates[1]),
        "x2": float(coordinates[2]),
        "y2": float(coordinates[3])
    }


def get_coordinate_string_from_url(url):
    removed_zoom_value = url[:url.index("_rect")]
    return removed_zoom_value[removed_zoom_value.rindex("/") + 1:]
