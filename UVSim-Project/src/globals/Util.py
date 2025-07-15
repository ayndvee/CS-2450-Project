import os
class Globals:
    MAX_VALUE = 9999
    MIN_VALUE = -9999
    STOP = '-99999'
    MEMORYSIZE = 100

    DEFAULT_PRIMARY = "#4C721D"
    DEFAULT_OFF = "#FFFFFF"

    CONFIG_FILE = CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    INTERVAL = 500