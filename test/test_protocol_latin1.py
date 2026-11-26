"""Exercise the real plaintext protocol, framing, checksum and value parser."""
from unittest import TestCase
from unittest.mock import Mock

from dsmr_parser.clients.protocol import create_dsmr_protocol
from dsmr_parser.parsers import TelegramParser
from test.example_telegrams import TELEGRAM_V5


class Latin1ProtocolTest(TestCase):
    def setUp(self):
        self.received = Mock()
        factory, _ = create_dsmr_protocol('5', telegram_callback=self.received)
        self.protocol = factory()

    @staticmethod
    def telegram(byte):
        # Model a text-message field containing the non-ASCII bytes reported in
        # #191 and #80, while retaining the original fixture's measurements.
        body = TELEGRAM_V5.split('!')[0] + f'0-0:96.13.0({chr(byte)})\r\n!'
        return (body + f'{TelegramParser.crc16(body):04X}\r\n').encode('latin1')

    def test_valid_latin1_frames_keep_checksum_and_measurements(self):
        for byte in (0xb0, 0xb3, 0xff):
            with self.subTest(byte=byte):
                self.received.reset_mock()
                data = self.telegram(byte)
                # Split immediately before the non-ASCII byte, as serial reads
                # need not contain whole lines or telegrams.
                split = data.index(bytes([byte]))
                self.protocol.data_received(data[:split])
                self.received.assert_not_called()
                self.protocol.data_received(data[split:])
                self.received.assert_called_once()
                telegram = self.received.call_args.args[0]
                self.assertEqual(telegram.P1_MESSAGE_HEADER.value, '50')
                self.assertEqual(float(telegram.INSTANTANEOUS_VOLTAGE_L1.value), 230.0)

    def test_corrupt_latin1_frame_is_dropped_and_next_ascii_frame_is_parsed(self):
        data = self.telegram(0xb0).replace(b'0230.0*V', b'0231.0*V')
        with self.assertLogs('dsmr_parser.clients.protocol', level='INFO') as logs:
            self.protocol.data_received(data + TELEGRAM_V5.encode('ascii'))
        self.assertIn('CRC', '\n'.join(logs.output))
        self.received.assert_called_once()
        self.assertEqual(float(self.received.call_args.args[0].INSTANTANEOUS_VOLTAGE_L1.value), 230.0)

    def test_non_ascii_padding_outside_telegram_is_ignored(self):
        self.protocol.data_received(b'\xff\xb0' + TELEGRAM_V5.encode('ascii') + b'\xff')
        self.received.assert_called_once()
