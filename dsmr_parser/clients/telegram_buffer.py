import re

# - Match all characters after start of telegram except for the start
# itself again '^\/]+', which eliminates incomplete preceding telegrams.
# - Do non greedy match using '?' so start is matched up to the first
# checksum that's found.
# - The checksum is optional '{0,4}' because not all telegram versions
# support it.
_FIND_TELEGRAMS_REGEX = re.compile(r"\/[^\/]+?\![A-F0-9]{0,4}\0?\r\n", re.DOTALL)


class TelegramBuffer(object):
    """
    Used as a buffer for a stream of telegram data. Constructs full telegram
    strings from the buffered data and returns it.
    """

    def __init__(self):
        self._buffer = ""

    def get_all(self):
        """
        Remove complete telegrams from buffer and yield them.
        :rtype generator:
        """
        for telegram in _FIND_TELEGRAMS_REGEX.findall(self._buffer):
            self._remove(telegram)
            yield telegram

    def append(self, data):
        """
        Add telegram data to buffer.
        :param str data: chars, lines or full telegram strings of telegram data
        """
        self._buffer += data

    def _remove(self, telegram):
        """
        Remove telegram from buffer and incomplete data preceding it. This
        is easier than validating the data before adding it to the buffer.
        :param str telegram:
        :return:
        """
        # Remove data leading up to the telegram and the telegram itself.
        index = self._buffer.index(telegram) + len(telegram)

        self._buffer = self._buffer[index:]


class EncryptedTelegramBuffer(object):
    """
    Used as a buffer for a stream of encrypted (DLMS general-global-cipher)
    telegram data.

    Encrypted telegrams (e.g. Luxembourg Smarty, Austrian Sagemcom) are not
    delimited by the '/...!XXXX' framing of plain telegrams. They are binary
    DLMS APDUs that start with the general-global-cipher tag (0xDB) and carry
    their own length, so they are framed by parsing that length rather than by
    a regex. Complete frames are yielded as hex strings, which is the format
    expected by ``TelegramParser.parse``.
    """

    GENERAL_GLOBAL_CIPHER_TAG = 0xDB
    # Long form length indicator: the following 2 bytes hold the length.
    LONG_FORM_LENGTH_INDICATOR = 0x82

    def __init__(self):
        self._buffer = bytearray()

    def get_all(self):
        """
        Remove complete frames from the buffer and yield them as hex strings.
        :rtype generator:
        """
        for frame in iter(self._take_frame, None):
            yield frame.hex()

    def append(self, data):
        """
        Add binary telegram data to buffer.
        :param bytes data: raw bytes read from the transport
        """
        self._buffer.extend(data)

    def _take_frame(self):
        """
        Remove and return the first complete frame from the buffer, or None
        when no complete frame is available yet.
        :rtype bytes or None:
        """
        while True:
            # Resync: discard anything before the first cipher tag.
            start = self._buffer.find(self.GENERAL_GLOBAL_CIPHER_TAG)
            if start == -1:
                self._buffer.clear()
                return None
            if start > 0:
                del self._buffer[:start]

            # tag (1) + system title length (1) + system title (n)
            #     + length indicator (1) + length (2)
            if len(self._buffer) < 2:
                return None
            system_title_length = self._buffer[1]
            header_length = 2 + system_title_length + 1 + 2
            if len(self._buffer) < header_length:
                return None

            if self._buffer[2 + system_title_length] != self.LONG_FORM_LENGTH_INDICATOR:
                # Not a frame we understand; drop this tag byte and resync.
                del self._buffer[:1]
                continue

            payload_length = int.from_bytes(
                self._buffer[3 + system_title_length:header_length], "big"
            )
            frame_length = header_length + payload_length
            if len(self._buffer) < frame_length:
                return None

            frame = bytes(self._buffer[:frame_length])
            del self._buffer[:frame_length]
            return frame
