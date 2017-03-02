class ParseError(Exception):
    pass


class InvalidChecksumError(ParseError):
    pass


class TelegramSpecificationMatchError(ParseError):
    pass
