import dsmr_parser.obis_name_mapping
import datetime


class Telegram(object):
    """
    Container for raw and parsed telegram data.
    Initializing:
        from dsmr_parser import telegram_specifications
        from dsmr_parser.exceptions import InvalidChecksumError, ParseError
        from dsmr_parser.objects import CosemObject, MBusObject, Telegram
        from dsmr_parser.parsers import TelegramParser
        from test.example_telegrams import TELEGRAM_V4_2
        parser = TelegramParser(telegram_specifications.V4)
        telegram = Telegram(TELEGRAM_V4_2, parser, telegram_specifications.V4)

    Attributes can be accessed on a telegram object by addressing by their english name, for example:
        telegram.ELECTRICITY_USED_TARIFF_1

    All attributes in a telegram can be iterated over, for example:
        [k for k,v in telegram]
    yields:
    ['P1_MESSAGE_HEADER',  'P1_MESSAGE_TIMESTAMP', 'EQUIPMENT_IDENTIFIER', ...]
    """
    def __init__(self, telegram_data, telegram_parser, telegram_specification):
        self._telegram_data = telegram_data
        self._telegram_specification = telegram_specification
        self._telegram_parser = telegram_parser
        self._obis_name_mapping = dsmr_parser.obis_name_mapping.EN
        self._reverse_obis_name_mapping = dsmr_parser.obis_name_mapping.REVERSE_EN
        self._dictionary = self._telegram_parser.parse(telegram_data)
        self._item_names = self._get_item_names()

    def __getattr__(self, name):
        ''' will only get called for undefined attributes '''
        obis_reference = self._reverse_obis_name_mapping[name]
        value = self._dictionary[obis_reference]
        setattr(self, name, value)
        return value

    def _get_item_names(self):
        return [self._obis_name_mapping[k] for k, v in self._dictionary.items()]

    def __iter__(self):
        for attr in self._item_names:
            value = getattr(self, attr)
            yield attr, value

    def __str__(self):
        output = ""
        for attr, value in self:
            output += "{}: \t {}\n".format(attr, str(value))
        return output


class DSMRObject(object):
    """
    Represents all data from a single telegram line.
    """

    def __init__(self, values):
        self.values = values


class MBusObject(DSMRObject):

    @property
    def datetime(self):
        return self.values[0]['value']

    @property
    def value(self):
        # TODO temporary workaround for DSMR v2.2. Maybe use the same type of
        # TODO object, but let the parse set them differently? So don't use
        # TODO hardcoded indexes here.
        if len(self.values) != 2:  # v2
            return self.values[6]['value']
        else:
            return self.values[1]['value']

    @property
    def unit(self):
        # TODO temporary workaround for DSMR v2.2. Maybe use the same type of
        # TODO object, but let the parse set them differently? So don't use
        # TODO hardcoded indexes here.
        if len(self.values) != 2:  # v2
            return self.values[5]['value']
        else:
            return self.values[1]['unit']

    def __str__(self):
        output = "{}\t[{}] at {}".format(str(self.value), str(self.unit), str(self.datetime.astimezone().isoformat()))
        return output


class CosemObject(DSMRObject):

    @property
    def value(self):
        return self.values[0]['value']

    @property
    def unit(self):
        return self.values[0]['unit']

    def __str__(self):
        print_value = self.value
        if isinstance(self.value, datetime.datetime):
            print_value = self.value.astimezone().isoformat()
        output = "{}\t[{}]".format(str(print_value), str(self.unit))
        return output


class ProfileGenericObject(DSMRObject):
    """
    Represents all data in a GenericProfile value.
    All buffer values are returned as a list of MBusObjects,
    containing the datetime (timestamp) and the value.
    """

    def __init__(self, values):
        super().__init__(values)
        self._buffer_list = None

    @property
    def buffer_length(self):
        return self.values[0]['value']

    @property
    def buffer_type(self):
        return self.values[1]['value']

    @property
    def buffer(self):
        if self._buffer_list is None:
            self._buffer_list = []
            values_offset = 2
            for i in range(self.buffer_length):
                offset = values_offset + i*2
                self._buffer_list.append(MBusObject([self.values[offset], self.values[offset + 1]]))
        return self._buffer_list

    @property
    def value(self):
        list = [['buffer_length', self.buffer_length]]
        list.append(['buffer_type', self.buffer_type])
        buffer_repr = [
            dict([['datetime', buffer_item.datetime],
             ['value', buffer_item.value]])
            for buffer_item in self.buffer
        ]
        list.append(['buffer', buffer_repr])
        return dict(list)

    def __str__(self):
        output = "\t buffer length: {}\n".format(self.buffer_length)
        output += "\t buffer type: {}".format(self.buffer_type)
        for buffer_value in self.buffer:
            timestamp = buffer_value.datetime
            if isinstance(timestamp, datetime.datetime):
                timestamp = str(timestamp.astimezone().isoformat())
            output += "\n\t event occured at: {}".format(timestamp)
            output += "\t for: {} [{}]".format(buffer_value.value, buffer_value.unit)
        return output
