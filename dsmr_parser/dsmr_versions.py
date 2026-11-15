"""List of supported DSMR versions."""

from dsmr_parser import telegram_specifications
from dsmr_parser.clients.settings import SERIAL_SETTINGS_V2_2, \
    SERIAL_SETTINGS_V4, SERIAL_SETTINGS_V5

DSMR_VERSIONS = {
    '2.2': (telegram_specifications.V2_2, SERIAL_SETTINGS_V2_2),
    '4': (telegram_specifications.V4, SERIAL_SETTINGS_V4),
    '4+': (telegram_specifications.V5, SERIAL_SETTINGS_V4),
    '5': (telegram_specifications.V5, SERIAL_SETTINGS_V5),
    '5B': (telegram_specifications.BELGIUM_FLUVIUS, SERIAL_SETTINGS_V5),
    '5L': (telegram_specifications.LUXEMBOURG_SMARTY, SERIAL_SETTINGS_V5),
    '5S': (telegram_specifications.SWEDEN, SERIAL_SETTINGS_V5),
    'Q3D': (telegram_specifications.Q3D, SERIAL_SETTINGS_V5),
    'ISKRA_IE': (telegram_specifications.ISKRA_IE, SERIAL_SETTINGS_V5),
    '5EONHU': (telegram_specifications.EON_HUNGARY, SERIAL_SETTINGS_V5),
    'MSn': (telegram_specifications.MSN, SERIAL_SETTINGS_V5),
    'SAGEMCOM_T210_D_R': (telegram_specifications.SAGEMCOM_T210_D_R, SERIAL_SETTINGS_V5),
}
