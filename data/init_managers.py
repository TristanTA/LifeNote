from data.managers.store_raw import RawData

def init_managers():
    raw_data_manager = RawData()
    return {
        "raw_data_manager": raw_data_manager
    }