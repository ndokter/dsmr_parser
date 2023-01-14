from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParser
from example_telegrams import TELEGRAM_V4_2
parser = TelegramParser(telegram_specifications.V4)
telegram = parser.parse(TELEGRAM_V4_2)

print(telegram)
