from collections import defaultdict
from decimal import Decimal
from operator import attrgetter

import datetime
import json

import pytz

from dsmr_parser import obis_name_mapping


class Telegram(object):
    """
    Container for parsed telegram data.

    Attributes can be accessed on a telegram object by addressing by their english name, for example:
        telegram.ELECTRICITY_USED_TARIFF_1

    All attributes in a telegram can be iterated over, for example:
        [k for k,v in telegram]
    yields:
    ['P1_MESSAGE_HEADER',  'P1_MESSAGE_TIMESTAMP', 'EQUIPMENT_IDENTIFIER', ...]
    """
    def __init__(self):
        self._telegram_data = defaultdict(list)
        self._mbus_channel_devices = {}
        self._item_names = []

    def add(self, obis_reference, dsmr_object):
        self._telegram_data[obis_reference].append(dsmr_object)

        # Update name mapping used to get value by attribute. Example: telegram.P1_MESSAGE_HEADER
        # Also keep track of the added names internally
        obis_name = obis_name_mapping.EN[obis_reference]
        setattr(self, obis_name, dsmr_object)
        if obis_name not in self._item_names:  # TODO solve issue with repeating obis references
            self._item_names.append(obis_name)

        # Group Mbus related values into a MbusDevice object.
        # TODO MaxDemandParser (BELGIUM_MAXIMUM_DEMAND_13_MONTHS) returns a list
        if isinstance(dsmr_object, DSMRObject) and dsmr_object.is_mbus_reading:
            self._add_mbus(obis_reference, dsmr_object)

    def _add_mbus(self, obis_reference, dsmr_object):
        """
        The given DsmrObject is assumed to be Mbus related and will be grouped into a MbusDevice.
        Grouping is done by the DsmrObject channel ID.
        """
        channel_id = dsmr_object.obis_id_code[1]

        # Create new MbusDevice for the first record on this channel_id
        if channel_id not in self._mbus_channel_devices:
            self._mbus_channel_devices[channel_id] = MbusDevice(channel_id=channel_id)

        mbus_device = self._mbus_channel_devices[channel_id]
        mbus_device.add(obis_reference, dsmr_object)

    def get_mbus_devices(self):
        """
        Return MbusDevice objects which are used for water, heat and gas meters.
        """
        mbus_devices = self._mbus_channel_devices.values()
        mbus_devices = sorted(mbus_devices, key=attrgetter('channel_id'))

        return mbus_devices

    def get_mbus_device_by_channel(self, channel_id):
        return self._mbus_channel_devices.get(channel_id)

    def __getitem__(self, obis_reference):
        """
        Deprecated method to get obis_reference by key. Exists for backwards compatibility

        Example: telegram[obis_references.P1_MESSAGE_HEADER]
        """
        try:
            # TODO use _telegram_data here or else TelegramParserFluviusTest.test_parse breaks
            return self._telegram_data[obis_reference][0]
            # obis_name = obis_name_mapping.EN[obis_reference]
            # return getattr(self, obis_name)
        except IndexError:
            # The index error is an internal detail. The KeyError is expected as a user.
            raise KeyError

    def __len__(self):
        return len(self._item_names)

    def __iter__(self):
        for attr in self._item_names:
            value = getattr(self, attr)
            yield attr, value

    def __str__(self):
        output = ""
        for attr, value in self:
            output += "{}: \t {}\n".format(attr, str(value))

        for channel_id, mbus_device in self._mbus_channel_devices.items():
            output += f'MBUS DEVICE (channel: {channel_id})\n'
            for obis_name, value in mbus_device:
                output += f'\t{obis_name}: \t {value} \n'

        return output

    def to_json(self):
        telegram_data = {obis_name: json.loads(value.to_json()) for obis_name, value in self}
        telegram_data['MBUS_DEVICES'] = [
            json.loads(mbus_device.to_json())
            for mbus_device in self._mbus_channel_devices.values()
        ]

        return json.dumps(telegram_data)


class DSMRObject(object):
    """
    Represents all data from a single telegram line.
    """
    def __init__(self, obis_id_code, values):
        self.obis_id_code = obis_id_code
        self.values = values

    @property
    def is_mbus_reading(self):
        """ Detect Mbus related readings using obis id + channel. """
        obis_id, channel_id = self.obis_id_code

        return obis_id == 0 and channel_id != 0


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
        output = "{}\t[{}] at {}".format(
            str(self.value),
            str(self.unit),
            str(self.datetime.astimezone().astimezone(pytz.utc).isoformat())
        )
        return output

    def to_json(self):
        timestamp = self.datetime
        if isinstance(self.datetime, datetime.datetime):
            timestamp = self.datetime.astimezone().astimezone(pytz.utc).isoformat()
        value = self.value
        if isinstance(self.value, datetime.datetime):
            value = self.value.astimezone().astimezone(pytz.utc).isoformat()
        if isinstance(self.value, Decimal):
            value = float(self.value)
        output = {
            'datetime': timestamp,
            'value': value,
            'unit': self.unit
        }
        return json.dumps(output)


class MBusObjectPeak(DSMRObject):

    @property
    def datetime(self):
        return self.values[0]['value']

    @property
    def occurred(self):
        return self.values[1]['value']

    @property
    def value(self):
        return self.values[2]['value']

    @property
    def unit(self):
        return self.values[2]['unit']

    def __str__(self):
        output = "{}\t[{}] at {} occurred {}"\
            .format(str(self.value), str(self.unit), str(self.datetime.astimezone().astimezone(pytz.utc).isoformat()),
                    str(self.occurred.astimezone().astimezone(pytz.utc).isoformat()))
        return output

    def to_json(self):
        timestamp = self.datetime
        if isinstance(self.datetime, datetime.datetime):
            timestamp = self.datetime.astimezone().astimezone(pytz.utc).isoformat()
        timestamp_occurred = self.occurred
        if isinstance(self.occurred, datetime.datetime):
            timestamp_occurred = self.occurred.astimezone().astimezone(pytz.utc).isoformat()
        value = self.value
        if isinstance(self.value, datetime.datetime):
            value = self.value.astimezone().astimezone(pytz.utc).isoformat()
        if isinstance(self.value, Decimal):
            value = float(self.value)
        output = {
            'datetime': timestamp,
            'occurred': timestamp_occurred,
            'value': value,
            'unit': self.unit
        }
        return json.dumps(output)


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
            print_value = self.value.astimezone().astimezone(pytz.utc).isoformat()
        output = "{}\t[{}]".format(str(print_value), str(self.unit))
        return output

    def to_json(self):
        json_value = self.value
        if isinstance(self.value, datetime.datetime):
            json_value = self.value.astimezone().astimezone(pytz.utc).isoformat()
        if isinstance(self.value, Decimal):
            json_value = float(self.value)
        output = {
            'value': json_value,
            'unit': self.unit
        }
        return json.dumps(output)


class ProfileGenericObject(DSMRObject):
    """
    Represents all data in a GenericProfile value.
    All buffer values are returned as a list of MBusObjects,
    containing the datetime (timestamp) and the value.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._buffer_list = None

    @property
    def value(self):
        # value is added to make sure the telegram iterator does not break
        return self.values

    @property
    def unit(self):
        # value is added to make sure all items have a unit so code that relies on that does not break
        return None

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
                offset = values_offset + i * 2
                self._buffer_list.append(
                    MBusObject(
                        obis_id_code=self.obis_id_code,
                        values=[self.values[offset], self.values[offset + 1]]
                    )
                )

        return self._buffer_list

    def __str__(self):
        output = "\t buffer length: {}\n".format(self.buffer_length)
        output += "\t buffer type: {}".format(self.buffer_type)
        for buffer_value in self.buffer:
            timestamp = buffer_value.datetime
            if isinstance(timestamp, datetime.datetime):
                timestamp = str(timestamp.astimezone().astimezone(pytz.utc).isoformat())
            output += "\n\t event occured at: {}".format(timestamp)
            output += "\t for: {} [{}]".format(buffer_value.value, buffer_value.unit)
        return output

    def to_json(self):
        """
        :return: A json of all values in the GenericProfileObject , with the following structure
                 {'buffer_length': n,
                  'buffer_type': obis_ref,
                  'buffer': [{'datetime': d1,
                              'value': v1,
                              'unit': u1},
                              ...
                               {'datetime': dn,
                              'value': vn,
                              'unit': un}
                              ]
                  }
        """
        list = [['buffer_length', self.buffer_length]]
        list.append(['buffer_type', self.buffer_type])
        buffer_repr = [json.loads(buffer_item.to_json()) for buffer_item in self.buffer]
        list.append(['buffer', buffer_repr])
        output = dict(list)
        return json.dumps(output)


class MbusDevice:
    """
    This object is similar to the Telegram except that it only contains readings related to the same mbus device.
    """

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self._item_names = []

    def add(self, obis_reference, dsmr_object):
        # Update name mapping used to get value by attribute. Example: telegram.P1_MESSAGE_HEADER
        # Also keep track of the added names internally
        obis_name = obis_name_mapping.EN[obis_reference]
        setattr(self, obis_name, dsmr_object)
        self._item_names.append(obis_name)

    def __len__(self):
        return len(self._item_names)

    def __iter__(self):
        for attr in self._item_names:
            value = getattr(self, attr)
            yield attr, value

    def __str__(self):
        output = "CHANNEL_ID: \t {}\n".format(self.channel_id)
        for attr, value in self:
            output += "{}: \t {}\n".format(attr, str(value))
        return output

    def to_json(self):
        data = {obis_name: json.loads(value.to_json()) for obis_name, value in self}
        data['CHANNEL_ID'] = self.channel_id

        return json.dumps(data)
