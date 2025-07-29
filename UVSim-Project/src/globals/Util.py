import os
class Globals:
    MAX_VALUE = 9999
    MIN_VALUE = -9999
    STOP = '-99999'
    MEMORYSIZE = 100
    MEMORYSIZE_LARGE = 250

    MINWORDLEN = 4
    MAXWORDLEN = 6

    DEFAULT_PRIMARY = "#4C721D"
    DEFAULT_OFF = "#FFFFFF"

    CONFIG_FILE = CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    INTERVAL = 500

    MODULO = 10000
    MODULO_LARGE = 1000000

    DIVMOD_SMALL = 100
    DIVMOD_LARGE = 1000

    MEMORY_TABLE_SIZE = 10
    