from dsmr_parser import telegram_specifications
from dsmr_parser.objects import Telegram
from dsmr_parser.parsers import TelegramParser
from example_telegrams import TELEGRAM_V4_2
parser = TelegramParser(telegram_specifications.V4)
telegram = Telegram(TELEGRAM_V4_2, parser, telegram_specifications.V4)

print(telegram)
