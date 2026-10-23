# Formatos de data e hora brasileiros para pt_BR
DATE_FORMAT = "d/m/Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "d/m/Y H:i"
YEAR_MONTH_FORMAT = "m/Y"
MONTH_DAY_FORMAT = "d/m"
SHORT_DATE_FORMAT = "d/m/Y"
SHORT_DATETIME_FORMAT = "d/m/Y H:i"
FIRST_DAY_OF_WEEK = 0  # Domingo

DATE_INPUT_FORMATS = [
    "%d/%m/%Y",  # '25/10/2026'
    "%d/%m/%y",  # '25/10/26'
    "%Y-%m-%d",  # '2026-10-25'
]

TIME_INPUT_FORMATS = [
    "%H:%M:%S",
    "%H:%M",
]

DATETIME_INPUT_FORMATS = [
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
]

DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = "."
NUMBER_GROUPING = 3
