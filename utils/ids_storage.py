class DataStorage:
    __instance = None

    @staticmethod
    def getInstance():
        if DataStorage.__instance is None:
            DataStorage()
        return DataStorage.__instance

    def __init__(self):
        if DataStorage.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DataStorage.__instance = self
            self.home_ids = {}

    def set_storage(self, data):
        self.home_ids = data

    def add(self, home_id):
        if self.home_ids.get(home_id) is None:
            self.home_ids[home_id] = home_id

    def is_home_added(self, home_id):
        return self.home_ids.get(home_id) is None
